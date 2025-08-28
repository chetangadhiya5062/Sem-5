<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="food_list">
  <table>
    <tr style="background-color:#ccff00">
      <th>Food Item</th>
      <th>Carbs (g)</th>
      <th>Fiber (g)</th>
      <th>Fat (g)</th>
      <th>Energy (kj)</th>
    </tr>
    <xsl:for-each select="food_item">
      <xsl:choose>
        <xsl:when test="@type = 'grain'">
          <tr style="background-color:#cccc00">
            <td><xsl:value-of select="name"/></td>
            <td><xsl:value-of select="carbs_per_serving"/></td>
            <td><xsl:value-of select="fiber_per_serving"/></td>
            <td><xsl:value-of select="fat_per_serving"/></td>
            <td><xsl:value-of select="kj_per_serving"/></td>
          </tr>
        </xsl:when>
        <xsl:when test="@type = 'vegetable'">
          <tr style="background-color:#00cc00">
            <td><xsl:value-of select="name"/></td>
            <td><xsl:value-of select="carbs_per_serving"/></td>
            <td><xsl:value-of select="fiber_per_serving"/></td>
            <td><xsl:value-of select="fat_per_serving"/></td>
            <td><xsl:value-of select="kj_per_serving"/></td>
          </tr>
        </xsl:when>
        <xsl:otherwise>
          <tr style="background-color:#cccccc">
            <td><xsl:value-of select="name"/></td>
            <td><xsl:value-of select="carbs_per_serving"/></td>
            <td><xsl:value-of select="fiber_per_serving"/></td>
            <td><xsl:value-of select="fat_per_serving"/></td>
            <td><xsl:value-of select="kj_per_serving"/></td>
          </tr>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
  </table>
</xsl:template>

</xsl:stylesheet>