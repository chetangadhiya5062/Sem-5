<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="class">
	<html>
		<body>
			<xsl:apply-templates/>
		</body>
	</html>
	</xsl:template>
	
	<xsl:template match="student">
		<p><b><xsl:value-of select="."/></b></p><br/>
	</xsl:template>
	
	<xsl:template match="teacher">
		<p><u><xsl:value-of select="."/></u></p>
	</xsl:template>
		
</xsl:stylesheet>