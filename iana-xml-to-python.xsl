<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:iana="http://www.iana.org/assignments"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<!-- USE THIS FILE TO TRANSFORM THE XML TO Python -->

<xsl:output method="text" omit-xml-declaration="yes"></xsl:output>
  <xsl:template match="iana:registry"># This is a copy of IANA DNS SRV registry at:
# http://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xml
# source xml file updated on <xsl:value-of select="iana:updated"/>

UDP_SERVICES = {

<xsl:for-each select="iana:record">
<xsl:if test="iana:protocol='udp' and iana:name !=''">   "<xsl:value-of select="iana:name" />":'''<xsl:value-of select="iana:description" />''',
</xsl:if>
</xsl:for-each>
}

TCP_SERVICES = {

<xsl:for-each select="iana:record">
<xsl:if test="iana:protocol='tcp' and iana:name !=''">   "<xsl:value-of select="iana:name" />":'''<xsl:value-of select="iana:description" />''',
</xsl:if>
</xsl:for-each>
}

</xsl:template>

</xsl:stylesheet>
