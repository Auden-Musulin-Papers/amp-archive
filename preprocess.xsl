<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="#all"
    version="2.0">
    
    <xsl:output method="xml" encoding="UTF-8" media-type="text/plain" indent="no"/>

    
    <xsl:template match="node()|@*">
        <xsl:copy>
            <xsl:apply-templates select="node()|@*"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="tei:TEI">
        <xsl:text disable-output-escaping='yes'>&lt;?xml-model href="https://id.acdh.oeaw.ac.at/auden-musulin-papers/schema.rng"?&gt;</xsl:text>
        <xsl:text disable-output-escaping='yes'>&lt;?xml-model href="https://id.acdh.oeaw.ac.at/auden-musulin-papers/schema.odd"?&gt;</xsl:text>
        <xsl:copy>
            <xsl:apply-templates select="node()|@*"/>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>