<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
     xpath-default-namespace="http://www.tei-c.org/ns/1.0"
    xmlns="http://www.tei-c.org/ns/1.0"
    version="2.0">
    <xsl:output method="text"/>
    <xsl:strip-space elements="*"/>
    <xsl:template match="/TEI">%% The openany option is here just to remove the blank pages before a new chapter
\documentclass[11pt,openany]{book}

\usepackage{fontspec}
\setmainfont{DejaVu Serif}

\title{Exemplier Adams de Lasciva Roma}

\begin{document}
<xsl:for-each-group select="//div" group-by="./bibl[@corresp='#adams']/biblScope/text()">
    <xsl:sort select="number(current-grouping-key())"></xsl:sort>
    <xsl:text>\chapter{Adams, page </xsl:text>
    <xsl:value-of select="current-grouping-key()"/>
    <xsl:text>}</xsl:text>
    <xsl:apply-templates select="current-group()"/>
</xsl:for-each-group>
\end{document}
    </xsl:template>
    <xsl:template match="div">
        <xsl:text>\section{</xsl:text>
        <xsl:apply-templates select="./bibl[@type='source']"/>
        <xsl:text>}
\textbf{Tags:} </xsl:text><xsl:value-of select="replace(@ana, '#', '')"/>
<xsl:text>
</xsl:text><xsl:apply-templates select="*[not(self::bibl)]"/>
        
<xsl:if test="./bibl[@corresp!='#adams' and @corresp]">        
<xsl:text> 
Source:
\begin{itemize}
</xsl:text>
<xsl:for-each select="bibl[@corresp!='#adams' and @corresp]">
    <xsl:text>    \item </xsl:text><xsl:apply-templates select="."/>
</xsl:for-each>
<xsl:text>
\end{itemize}</xsl:text>
</xsl:if>
<xsl:text>

</xsl:text>
</xsl:template>
    <xsl:template match="bibl[@type!='source']"><xsl:apply-templates/></xsl:template>
    
    <xsl:template match="bibl[@type='source']"><xsl:apply-templates/></xsl:template>
    
    <xsl:template match="author[@xml:lang='fr']" ><xsl:apply-templates/></xsl:template>
    <xsl:template match="persName[@xml:lang='eng']" />
    <xsl:template match="title">\textit{<xsl:apply-templates/>}</xsl:template>
    <xsl:template match="idno"/>
    <xsl:template match="quote">
        <xsl:text>

\begin{quote}
``</xsl:text><xsl:apply-templates/><xsl:text>''
\end{quote}

</xsl:text>
    </xsl:template>
    <xsl:template match="w">
        <xsl:choose>
            <xsl:when test=" contains(./text(), '\{')"></xsl:when>
            <xsl:when test="@ana">\textbf{<xsl:apply-templates/>}</xsl:when>
            <xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
        </xsl:choose>
        <xsl:text> </xsl:text>
    </xsl:template>
    <xsl:template match="text()">
        <xsl:value-of select="replace(., '[\}\{\[\]\\]', ' ')"/>
    </xsl:template>
</xsl:stylesheet>