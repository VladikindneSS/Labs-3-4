<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text" encoding="UTF-8"/>
    <xsl:template match="/musicCatalog">
        <xsl:text>Сводка музыкального каталога
</xsl:text>
        <xsl:for-each select="album">
            <xsl:text>Альбом: </xsl:text><xsl:value-of select="title"/><xsl:text>
</xsl:text>
            <xsl:text>Исполнители: </xsl:text><xsl:for-each select="artists/artist">
                <xsl:value-of select="."/><xsl:if test="position() != last()">, </xsl:if>
            </xsl:for-each><xsl:text>
</xsl:text>
            <xsl:text>Жанры: </xsl:text><xsl:for-each select="genres/genre">
                <xsl:value-of select="."/><xsl:if test="position() != last()">, </xsl:if>
            </xsl:for-each><xsl:text>
</xsl:text>
            <xsl:text>Дата выпуска: </xsl:text><xsl:value-of select="releaseDate"/><xsl:text>
</xsl:text>
            <xsl:text>Возрастное ограничение: </xsl:text><xsl:value-of select="ageRestriction"/><xsl:text>
</xsl:text>
            <xsl:text>Композиции:
</xsl:text>
            <xsl:for-each select="tracks/track">
                <xsl:text>  - </xsl:text><xsl:value-of select="title"/> (<xsl:value-of select="duration div 60"/> мин <xsl:value-of select="duration mod 60"/> сек)<xsl:text>
</xsl:text>
            </xsl:for-each>
            <xsl:text>-------------------
</xsl:text>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>