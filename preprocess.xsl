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
        <xsl:choose>
            <xsl:when test=".//tei:body/tei:div[@type='transcription']/tei:div[@type='envelope' or @type='letter']">
                <xsl:text disable-output-escaping='yes'>&lt;?xml-model href="https://id.acdh.oeaw.ac.at/auden-musulin-papers/schema.rng"?&gt;</xsl:text>
                <xsl:text disable-output-escaping='yes'>&lt;?xml-model href="https://id.acdh.oeaw.ac.at/auden-musulin-papers/schema.odd"?&gt;</xsl:text>
            </xsl:when>
            <xsl:when test=".//tei:body/tei:div[@type='transcription']/tei:div[@type='prose']">
                <xsl:text disable-output-escaping='yes'>&lt;?xml-model href="https://id.acdh.oeaw.ac.at/auden-musulin-papers/schema-prose.rng"?&gt;</xsl:text>
                <xsl:text disable-output-escaping='yes'>&lt;?xml-model href="https://id.acdh.oeaw.ac.at/auden-musulin-papers/schema-prose.odd"?&gt;</xsl:text>
            </xsl:when>
            <xsl:when test=".//tei:body/tei:div[@type='transcription']/tei:div[@type='photo']">
                <xsl:text disable-output-escaping='yes'>&lt;?xml-model href="https://id.acdh.oeaw.ac.at/auden-musulin-papers/schema.rng"?&gt;</xsl:text>
                <xsl:text disable-output-escaping='yes'>&lt;?xml-model href="https://id.acdh.oeaw.ac.at/auden-musulin-papers/schema.odd"?&gt;</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text disable-output-escaping='yes'>&lt;?xml-model href="https://id.acdh.oeaw.ac.at/auden-musulin-papers/schema-indexes.rng"?&gt;</xsl:text>
                <xsl:text disable-output-escaping='yes'>&lt;?xml-model href="https://id.acdh.oeaw.ac.at/auden-musulin-papers/schema-indexes.odd"?&gt;</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:copy>
            <xsl:apply-templates select="node()|@*"/>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>