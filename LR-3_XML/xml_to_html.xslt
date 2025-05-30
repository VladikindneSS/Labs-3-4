<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/musicCatalog">
        <html>
            <head>
                <title>Музыкальный каталог</title>
                <style>
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        font-family: Arial, sans-serif;
                    }
                    th, td {
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }
                    th {
                        background-color: #4CAF50;
                        color: white;
                    }
                    tr:nth-child(even) {
                        background-color: #f2f2f2;
                    }
                    tr:hover {
                        background-color: #ddd;
                    }
                </style>
            </head>
            <body>
                <h2>Музыкальный каталог</h2>
                <table>
                    <tr>
                        <th>Название</th>
                        <th>Исполнители</th>
                        <th>Жанры</th>
                        <th>Дата выпуска</th>
                        <th>Возрастное ограничение</th>
                        <th>Композиции</th>
                    </tr>
                    <xsl:for-each select="album">
                        <tr>
                            <td><xsl:value-of select="title"/></td>
                            <td>
                                <xsl:for-each select="artists/artist">
                                    <xsl:value-of select="."/>
                                    <xsl:if test="position() != last()">, </xsl:if>
                                </xsl:for-each>
                            </td>
                            <td>
                                <xsl:for-each select="genres/genre">
                                    <xsl:value-of select="."/>
                                    <xsl:if test="position() != last()">, </xsl:if>
                                </xsl:for-each>
                            </td>
                            <td><xsl:value-of select="releaseDate"/></td>
                            <td><xsl:value-of select="ageRestriction"/></td>
                            <td>
                                <ul>
                                    <xsl:for-each select="tracks/track">
                                        <li><xsl:value-of select="title"/> (<xsl:value-of select="duration div 60"/> мин <xsl:value-of select="duration mod 60"/> сек)</li>
                                    </xsl:for-each>
                                </ul>
                            </td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>