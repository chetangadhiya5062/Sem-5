import pandas as pd

dir = "files/program_1"

df = pd.read_csv(f"{dir}/input.csv")  
df["Average"] = df.drop("Name", axis=1).mean(axis=1)  
df[["Name", "Average"]].to_csv(f"{dir}/output.csv", index=False)  
