import csv
import json
import logging
import random
import threading
import time
import uuid
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

# GUI imports

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    from tkinter import ttk
    from tkinter.scrolledtext import ScrolledText
except Exception:  # pragma: no cover - GUI optional
    # If Tkinter isn't available, the CLI path will still work
    tk = None  # type: ignore
    ttk = None  # type: ignore
    filedialog = None  # type: ignore
    messagebox = None  # type: ignore



def setup_logging(log_dir: Path | None = None, level: int = logging.DEBUG) -> logging.Logger:
    """Configure root logger with console and rotating file handlers.

    - Console: human-friendly stream handler
    - File: rotating file handler `lab7.log` up to ~1MB x 3 backups
    """
    logger = logging.getLogger("lab7")
    if logger.handlers:
        return logger  # already configured

    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    if log_dir is None:
        log_dir = Path(__file__).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    file_path = log_dir / "lab7.log"
    file_handler = RotatingFileHandler(file_path, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.debug("Logging configured. Console and file handlers are set.")
    return logger


def load_user_config(config_path: Path) -> Dict[str, Any]:
	"""Load a JSON configuration file.

	Logs I/O operations and exceptions. Returns defaults if file is missing/invalid.
	"""
	logger = logging.getLogger("lab7.config")
	logger.info("Loading configuration from %s", config_path)
	default_cfg: Dict[str, Any] = {"max_retries": 2, "backoff_seconds": 0.2}
	if not config_path.exists():
		logger.warning("Config file not found. Using defaults: %s", default_cfg)
		return default_cfg
	try:
		with config_path.open("r", encoding="utf-8") as fp:
			cfg = json.load(fp)
			logger.debug("Config loaded: %s", cfg)
			return {**default_cfg, **cfg}
	except json.JSONDecodeError as err:
		logger.error("Invalid JSON in config: %s", err, exc_info=True)
		return default_cfg
	except OSError as err:
		logger.error("Failed reading config: %s", err, exc_info=True)
		return default_cfg


def read_numbers_from_csv(csv_path: Path) -> List[float]:
	"""Read numbers from a CSV file with one number per line.

	Demonstrates input logging and robust error handling.
	"""
	logger = logging.getLogger("lab7.io")
	logger.info("Reading numbers from %s", csv_path)
	if not csv_path.exists():
		logger.warning("CSV file not found. Falling back to dummy data.")
		return [1, 2, 3, 4, 5, -1, 0]
	values: List[float] = []
	try:
		with csv_path.open("r", encoding="utf-8") as fp:
			csv_reader = csv.reader(fp)
			for line_no, row in enumerate(csv_reader, start=1):
				if not row:  # Skip empty rows
					logger.debug("Skipping empty line %d", line_no)
					continue
				# Process each value in the row
				for value in row:
					text = value.strip()
					if not text:
						continue
					try:
						values.append(float(text))
					except ValueError:
						logger.warning("Non-numeric value on line %d: %r", line_no, text)
		logger.info("Loaded %d values", len(values))
		return values
	except OSError as err:
		logger.error("Failed reading CSV: %s", err, exc_info=True)
		return []


def transform_numbers(values: Iterable[float]) -> List[float]:
	"""Transform numbers with decisions and loop logging.

	- Negative values are clamped to 0 (decision point)
	- Even numbers are doubled, odd numbers are tripled (decision point)
	- Each iteration is traced at DEBUG level
	- Overall timing is recorded
	"""
	logger = logging.getLogger("lab7.transform")
	start = time.perf_counter()
	output: List[float] = []
	for index, value in enumerate(values):
		logger.debug("Processing index=%d value=%s", index, value)
		if value < 0:
			logger.warning("Negative input encountered at index=%d: %s; clamping to 0", index, value)
			value = 0
		if int(value) % 2 == 0:
			result = value * 2
			logger.debug("Even branch -> doubled: %s -> %s", value, result)
		else:
			result = value * 3
			logger.debug("Odd branch -> tripled: %s -> %s", value, result)
		output.append(result)
	elapsed_ms = (time.perf_counter() - start) * 1000
	logger.info("Transformed %d numbers in %.2f ms", len(output), elapsed_ms)
	return output


def compute_statistics(values: List[float]) -> Tuple[float, float]:
	"""Compute mean and max with error handling and logging."""
	logger = logging.getLogger("lab7.stats")
	logger.info("Computing statistics for %d values", len(values))
	if not values:
		logger.error("No values provided for statistics")
		return 0.0, float("nan")
	try:
		mean_value = sum(values) / len(values)
		max_value = max(values)
		logger.debug("Intermediate stats -> sum=%s count=%d max=%s", sum(values), len(values), max_value)
		logger.info("Stats computed: mean=%.3f max=%.3f", mean_value, max_value)
		return mean_value, max_value
	except ZeroDivisionError as err:
		logger.critical("Division by zero while computing stats: %s", err, exc_info=True)
		return 0.0, float("nan")


def call_external_service(payload: Dict[str, Any], max_retries: int, backoff_seconds: float) -> Dict[str, Any]:
	"""Simulate an external API call with retries and logging.

	Randomly fails to demonstrate WARNING/ERROR logs and retry behavior.
	"""
	logger = logging.getLogger("lab7.api")
	attempt = 0
	while True:
		attempt += 1
		request_id = uuid.uuid4().hex[:8]
		logger.info("Attempt %d | request_id=%s | Sending payload: %s", attempt, request_id, payload)
		# 30% chance of simulated failure
		if random.random() < 0.3:
			logger.error("Attempt %d | request_id=%s | Simulated network error", attempt, request_id)
			if attempt > max_retries:
				logger.critical("All retries exhausted for request_id=%s", request_id)
				raise ConnectionError("External service unreachable after retries")
			logger.warning("Retrying in %.2f seconds...", backoff_seconds)
			time.sleep(backoff_seconds)
			continue
		# Success path
		response = {"request_id": request_id, "status": 200, "echo": payload}
		logger.info("Attempt %d | request_id=%s | Response: %s", attempt, request_id, response)
		return response


def main() -> None:
	logger = setup_logging()
	logger.info("=== Lab 7: Implementing Logging Mechanism Demo ===")

	project_root = Path(__file__).parent
	csv_path = project_root / "numbers.csv"  # optional input
	config_path = project_root / "config.json"  # optional config

	# Load config (I/O and exception handling)
	cfg = load_user_config(config_path)
	max_retries = int(cfg.get("max_retries", 2))
	backoff_seconds = float(cfg.get("backoff_seconds", 0.2))
	logger.debug("Effective config -> max_retries=%d backoff_seconds=%.2f", max_retries, backoff_seconds)

	# Read input numbers (I/O)
	values = read_numbers_from_csv(csv_path)
	logger.info("Input values: %s", values)

	# Transform values (loops, decisions, timing)
	transformed = transform_numbers(values)
	logger.info("Transformed values: %s", transformed)

	# Compute statistics (decisions + errors)
	mean_value, max_value = compute_statistics(transformed)
	logger.info("Final stats -> mean=%.3f max=%.3f", mean_value, max_value)

	# Simulate external interaction (requests, retries)
	try:
		response = call_external_service(
			{"mean": mean_value, "max": max_value}, max_retries=max_retries, backoff_seconds=backoff_seconds
		)
		logger.info("External service success -> %s", response)
	except ConnectionError as err:
		logger.exception("External service failed: %s", err)

	logger.info("=== Demo complete ===")


class TextWidgetHandler(logging.Handler):
	"""Logging handler that writes log records to a Tkinter text widget."""

	def __init__(self, text_widget: "ScrolledText") -> None:  # type: ignore[name-defined]
		super().__init__()
		self.text_widget = text_widget
		self.text_widget.configure(state="disabled")

	def emit(self, record: logging.LogRecord) -> None:
		msg = self.format(record) + "\n"
		def append() -> None:
			self.text_widget.configure(state="normal")
			self.text_widget.insert("end", msg)
			self.text_widget.see("end")
			self.text_widget.configure(state="disabled")
		# Schedule in GUI thread
		self.text_widget.after(0, append)


class Lab7App:
	def __init__(self, root: "tk.Tk") -> None:  # type: ignore[name-defined]
		self.root = root
		self.root.title("Lab 7 · Logging Mechanism Demo")
		self.logger = setup_logging()
		self._init_style()
		# Initialize UI-bound variables BEFORE building UI
		self.worker: threading.Thread | None = None
		self.progress_var = tk.DoubleVar(value=0.0)
		self.mean_var = tk.StringVar(value="-")
		self.max_var = tk.StringVar(value="-")
		self.theme_mode = tk.StringVar(value="Light")
		self._build_ui()
		self._wire_logger()

	def _init_style(self) -> None:
		style = ttk.Style()
		try:
			style.theme_use("clam")
		except Exception:
			pass
		# Define base colors
		self._light_palette = {
			"bg": "#f7f7fb",
			"fg": "#222",
			"accent": "#4f46e5",
			"muted": "#6b7280",
			"panel": "#ffffff",
		}
		self._dark_palette = {
			"bg": "#0f172a",
			"fg": "#e5e7eb",
			"accent": "#60a5fa",
			"muted": "#94a3b8",
			"panel": "#111827",
		}
		self._apply_theme(self._light_palette)

	def _apply_theme(self, p: dict) -> None:
		style = ttk.Style()
		self.root.configure(bg=p["bg"]) 
		style.configure("TFrame", background=p["panel"]) 
		style.configure("Header.TFrame", background=p["bg"]) 
		style.configure("Toolbar.TFrame", background=p["panel"]) 
		style.configure("TLabel", background=p["panel"], foreground=p["fg"]) 
		style.configure("Header.TLabel", background=p["bg"], foreground=p["fg"], font=("Segoe UI", 14, "bold")) 
		style.configure("Sub.TLabel", background=p["bg"], foreground=p["muted"], font=("Segoe UI", 9)) 
		style.configure("TButton", padding=6)
		style.map("TButton", foreground=[("active", p["fg"])])
		style.configure("Accent.TButton", background=p["accent"], foreground="#fff")
		style.configure("TEntry", fieldbackground="#ffffff")
		style.configure("TNotebook", background=p["bg"])  # tabposition is a widget option, not style
		style.configure("TNotebook.Tab", padding=(14, 8), background=p["panel"]) 
		style.configure("Status.TLabel", background=p["panel"], foreground=p["muted"]) 
		style.configure("Horizontal.TProgressbar", thickness=8)

	def _build_ui(self) -> None:
		# Menubar
		self._build_menubar()

		# Header
		header = ttk.Frame(self.root, style="Header.TFrame")
		header.grid(row=0, column=0, columnspan=2, sticky="ew")
		title = ttk.Label(header, text="Logging Mechanism Demo", style="Header.TLabel")
		title.grid(row=0, column=0, padx=12, pady=(10, 2), sticky="w")
		sub = ttk.Label(header, text="Analyze · Transform · Stats · External Call", style="Sub.TLabel")
		sub.grid(row=1, column=0, padx=12, pady=(0, 10), sticky="w")

		# Toolbar
		toolbar = ttk.Frame(self.root, style="Toolbar.TFrame")
		toolbar.grid(row=1, column=0, columnspan=2, sticky="ew")
		self.run_btn = ttk.Button(toolbar, text="Run", command=self._on_run, style="Accent.TButton")
		self.run_btn.grid(row=0, column=0, padx=8, pady=8)
		self.save_cfg_btn = ttk.Button(toolbar, text="Save Config", command=self._on_save_config)
		self.save_cfg_btn.grid(row=0, column=1, padx=4, pady=8)
		self.clear_btn = ttk.Button(toolbar, text="Clear Logs", command=self._on_clear_logs)
		self.clear_btn.grid(row=0, column=2, padx=4, pady=8)
		self.theme_btn = ttk.Button(toolbar, text="Dark Mode", command=self._toggle_theme)
		self.theme_btn.grid(row=0, column=3, padx=8, pady=8)

		# Notebook
		nb = ttk.Notebook(self.root)
		nb.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
		self.root.rowconfigure(2, weight=1)
		self.root.columnconfigure(0, weight=1)

		# Tab: Inputs
		inputs = ttk.Frame(nb)
		nb.add(inputs, text="Inputs")
		inputs.columnconfigure(1, weight=1)
		ttk.Label(inputs, text="CSV File (optional)").grid(row=0, column=0, sticky="w", padx=8, pady=8)
		self.csv_var = tk.StringVar()
		ent_csv = ttk.Entry(inputs, textvariable=self.csv_var)
		ent_csv.grid(row=0, column=1, sticky="ew", padx=8, pady=8)
		btn_csv = ttk.Button(inputs, text="Browse", command=self._browse_csv)
		btn_csv.grid(row=0, column=2, padx=8, pady=8)

		ttk.Label(inputs, text="Config File (optional)").grid(row=1, column=0, sticky="w", padx=8, pady=8)
		self.cfg_var = tk.StringVar()
		ent_cfg = ttk.Entry(inputs, textvariable=self.cfg_var)
		ent_cfg.grid(row=1, column=1, sticky="ew", padx=8, pady=8)
		btn_cfg = ttk.Button(inputs, text="Browse", command=self._browse_cfg)
		btn_cfg.grid(row=1, column=2, padx=8, pady=8)

		ttk.Label(inputs, text="Max retries").grid(row=2, column=0, sticky="w", padx=8, pady=8)
		self.retries_var = tk.IntVar(value=2)
		sp_retries = ttk.Spinbox(inputs, from_=0, to=10, textvariable=self.retries_var, width=8)
		sp_retries.grid(row=2, column=1, sticky="w", padx=8, pady=8)

		ttk.Label(inputs, text="Backoff (sec)").grid(row=2, column=2, sticky="w", padx=8, pady=8)
		self.backoff_var = tk.DoubleVar(value=0.2)
		sp_backoff = ttk.Spinbox(inputs, from_=0.0, to=10.0, increment=0.1, textvariable=self.backoff_var, width=8)
		sp_backoff.grid(row=2, column=3, sticky="w", padx=8, pady=8)

		# Tab: Logs
		logs = ttk.Frame(nb)
		nb.add(logs, text="Logs")
		self.log_text = ScrolledText(logs, height=22, width=100, state="disabled")
		self.log_text.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
		logs.rowconfigure(0, weight=1)
		logs.columnconfigure(0, weight=1)

		# Tab: Results
		results = ttk.Frame(nb)
		nb.add(results, text="Results")
		results.columnconfigure(1, weight=1)
		ttk.Label(results, text="Mean").grid(row=0, column=0, sticky="w", padx=8, pady=8)
		ttk.Label(results, textvariable=self.mean_var).grid(row=0, column=1, sticky="w", padx=8, pady=8)
		ttk.Label(results, text="Max").grid(row=1, column=0, sticky="w", padx=8, pady=8)
		ttk.Label(results, textvariable=self.max_var).grid(row=1, column=1, sticky="w", padx=8, pady=8)

		# Status bar with progress
		status_bar = ttk.Frame(self.root, style="Toolbar.TFrame")
		status_bar.grid(row=3, column=0, columnspan=2, sticky="ew")
		self.status_var = tk.StringVar(value="Ready")
		lbl_status = ttk.Label(status_bar, textvariable=self.status_var, style="Status.TLabel")
		lbl_status.grid(row=0, column=0, sticky="w", padx=8, pady=6)
		self.progress = ttk.Progressbar(status_bar, mode="determinate", variable=self.progress_var, maximum=100)
		self.progress.grid(row=0, column=1, sticky="e", padx=8, pady=6)
		status_bar.columnconfigure(0, weight=1)

	def _build_menubar(self) -> None:
		menubar = tk.Menu(self.root)
		m_file = tk.Menu(menubar, tearoff=0)
		m_file.add_command(label="Open CSV...", command=self._browse_csv)
		m_file.add_command(label="Open Config...", command=self._browse_cfg)
		m_file.add_separator()
		m_file.add_command(label="Save Config", command=self._on_save_config)
		m_file.add_separator()
		m_file.add_command(label="Exit", command=self.root.quit)
		menubar.add_cascade(label="File", menu=m_file)

		m_view = tk.Menu(menubar, tearoff=0)
		m_view.add_command(label="Light Mode", command=lambda: self._set_theme("Light"))
		m_view.add_command(label="Dark Mode", command=lambda: self._set_theme("Dark"))
		menubar.add_cascade(label="View", menu=m_view)

		m_help = tk.Menu(menubar, tearoff=0)
		m_help.add_command(label="About", command=self._show_about)
		menubar.add_cascade(label="Help", menu=m_help)
		self.root.config(menu=menubar)

	def _set_theme(self, mode: str) -> None:
		self.theme_mode.set(mode)
		if mode == "Dark":
			self._apply_theme(self._dark_palette)
			self.theme_btn.configure(text="Light Mode")
		else:
			self._apply_theme(self._light_palette)
			self.theme_btn.configure(text="Dark Mode")

	def _toggle_theme(self) -> None:
		self._set_theme("Dark" if self.theme_mode.get() == "Light" else "Light")

	def _show_about(self) -> None:
		messagebox and messagebox.showinfo(
			"About",
			"Lab 7 - Logging Mechanism Demo\n\n"
			"Demonstrates structured logging at I/O, loops, decisions, exceptions, and retries.\n"
			"GUI with live log viewer, progress, theming, and results panel.",
		)

	def _wire_logger(self) -> None:
		self.gui_handler = TextWidgetHandler(self.log_text)
		self.gui_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s", "%H:%M:%S"))
		logging.getLogger("lab7").addHandler(self.gui_handler)
		logging.getLogger("lab7.config").addHandler(self.gui_handler)
		logging.getLogger("lab7.io").addHandler(self.gui_handler)
		logging.getLogger("lab7.transform").addHandler(self.gui_handler)
		logging.getLogger("lab7.stats").addHandler(self.gui_handler)
		logging.getLogger("lab7.api").addHandler(self.gui_handler)

	def _browse_csv(self) -> None:
		if filedialog is None:
			return
		path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv"), ("All", "*.*")])
		if path:
			self.csv_var.set(path)

	def _browse_cfg(self) -> None:
		if filedialog is None:
			return
		path = filedialog.askopenfilename(filetypes=[("JSON", "*.json"), ("All", "*.*")])
		if path:
			self.cfg_var.set(path)

	def _on_clear_logs(self) -> None:
		self.log_text.configure(state="normal")
		self.log_text.delete("1.0", "end")
		self.log_text.configure(state="disabled")

	def _on_save_config(self) -> None:
		cfg_path = self.cfg_var.get().strip()
		if not cfg_path:
			messagebox and messagebox.showwarning("Save Config", "Please choose a config file path (JSON)")
			return
		cfg = {"max_retries": self.retries_var.get(), "backoff_seconds": self.backoff_var.get()}
		try:
			Path(cfg_path).write_text(json.dumps(cfg, indent=2), encoding="utf-8")
			messagebox and messagebox.showinfo("Save Config", f"Saved config to\n{cfg_path}")
		except OSError as err:
			messagebox and messagebox.showerror("Save Config", f"Failed to save config: {err}")

	def _on_run(self) -> None:
		if self.worker and self.worker.is_alive():
			return
		self.run_btn.configure(state="disabled")
		self.status_var.set("Running...")
		self.progress_var.set(0)
		self.worker = threading.Thread(target=self._run_pipeline_bg, daemon=True)
		self.worker.start()

	def _run_pipeline_bg(self) -> None:
		try:
			project_root = Path(__file__).parent
			csv_path = Path(self.csv_var.get()) if self.csv_var.get().strip() else project_root / "numbers.csv"
			cfg_path = Path(self.cfg_var.get()) if self.cfg_var.get().strip() else project_root / "config.json"

			cfg_file = load_user_config(cfg_path)
			# Override with UI
			cfg_file["max_retries"] = int(self.retries_var.get())
			cfg_file["backoff_seconds"] = float(self.backoff_var.get())
			self.logger.debug("GUI effective config -> %s", cfg_file)
			self.root.after(0, lambda: self.progress_var.set(10))
			values = read_numbers_from_csv(csv_path)
			self.root.after(0, lambda: self.progress_var.set(35))
			transformed = transform_numbers(values)
			self.root.after(0, lambda: self.progress_var.set(65))
			mean_value, max_value = compute_statistics(transformed)
			def update_results() -> None:
				self.mean_var.set(f"{mean_value:.3f}")
				self.max_var.set(f"{max_value:.3f}")
			self.root.after(0, update_results)
			try:
				call_external_service({"mean": mean_value, "max": max_value}, cfg_file["max_retries"], cfg_file["backoff_seconds"])  # noqa: F841
			except ConnectionError as err:
				logging.getLogger("lab7").exception("External service failed: %s", err)
			finally:
				self.root.after(0, lambda: self.progress_var.set(100))
		finally:
			self.root.after(0, self._on_run_complete)

	def _on_run_complete(self) -> None:
		self.run_btn.configure(state="normal")
		self.status_var.set("Ready")


def launch_gui_or_cli() -> None:
	if tk is not None:
		root = tk.Tk()
		Lab7App(root)
		root.mainloop()
	else:
		main()


if __name__ == "__main__":
	launch_gui_or_cli()


