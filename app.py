# =============================================================
#  🎧 Hits de México en Spotify (2015–2025): panel interactivo
#  Ejecutar con:  streamlit run app.py
#  Requiere:      pip install -U streamlit pandas plotly
# =============================================================

import pandas as pd
import plotly.express as px
import streamlit as st

# -------------------------------------------------------------
# 1. Configuración de la página y paleta
# -------------------------------------------------------------
st.set_page_config(
    page_title="Hits de México en Spotify",
    page_icon="🎧",
    layout="wide",
)

# Paleta inspirada en los carteles fosforescentes de los bailes sonideros
ROSA = "#FF2E88"
AMARILLO = "#FFD23F"
CIAN = "#00C2D1"
NARANJA = "#FF7A1A"
VERDE = "#3BB273"
MORADO = "#7B2CBF"
AZUL = "#3A86FF"
GRIS = "#8D99AE"

# Cada género conserva su color en los tres gráficos
COLORES_GENERO = {
    "Corridos tumbados": ROSA,
    "Regional mexicano": NARANJA,
    "Reguetón": MORADO,
    "Pop latino": CIAN,
    "Pop en inglés": AZUL,
    "Urbano latino": AMARILLO,
    "Tropical": VERDE,
    "Rock/Alternativo": GRIS,
}
COLORES_SI_NO = {"Sí": ROSA, "No": GRIS}
COLOR_OTROS = "#C4C4D4"
SECUENCIA = [ROSA, CIAN, NARANJA, MORADO, AMARILLO, VERDE, AZUL, GRIS]
ESCALA_CONTINUA = [CIAN, MORADO, ROSA]

NOMBRES = {
    "artista_principal": "Artista",
    "genero_musical": "Género musical",
    "pais_artista": "País del artista",
    "anio_lanzamiento": "Año de lanzamiento",
    "sexo_artista": "Sexo del artista",
    "tipo_artista": "Tipo de artista",
    "origen_mexicano": "Origen mexicano",
    "es_colaboracion": "Colaboración",
    "viral_tiktok": "Viral en TikTok",
    "contenido_explicito": "Contenido explícito",
    "duracion_segundos": "Duración (segundos)",
    "bpm": "Tempo (BPM)",
    "bailabilidad": "Bailabilidad (0 a 1)",
    "energia": "Energía (0 a 1)",
    "porcentaje_streams_mexico": "% de streams desde México",
    "semanas_top50_mx": "Semanas en el Top 50 de México",
    "streams_totales_millones": "Streams totales (millones)",
    "streams_mexico_millones": "Streams en México (millones)",
}

COLUMNAS_BOOLEANAS = ["es_colaboracion", "contenido_explicito", "origen_mexicano", "viral_tiktok"]

# Barra de herramientas de Plotly: sin logo y sin herramientas de selección
CONFIG_PLOTLY = {"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d"]}


# -------------------------------------------------------------
# 2. Funciones de ayuda
# -------------------------------------------------------------
@st.cache_data
def cargar_datos(ruta: str) -> pd.DataFrame:
    """Lee el CSV y deja cada columna con su tipo correcto."""
    df = pd.read_csv(ruta)
    for col in COLUMNAS_BOOLEANAS:
        df[col] = df[col].astype(str).str.strip().str.upper() == "TRUE"
    df["fecha_lanzamiento"] = pd.to_datetime(df["fecha_lanzamiento"], errors="coerce")
    return df


def como_texto(serie: pd.Series) -> pd.Series:
    """True/False -> 'Sí'/'No' para que se lea bien en leyendas y tooltips."""
    if serie.dtype == bool:
        return serie.map({True: "Sí", False: "No"})
    return serie.astype(str)


def mapa_de_colores(columna):
    """Devuelve el mapa de colores fijo de una columna, si lo tiene."""
    if columna == "genero_musical":
        return COLORES_GENERO
    if columna in COLUMNAS_BOOLEANAS:
        return COLORES_SI_NO
    return {}


def dar_estilo(fig, alto: int = 440):
    """Estilo común. El fondo transparente funciona en modo claro y oscuro."""
    fig.update_layout(
        height=alto,
        margin=dict(l=8, r=8, t=40, b=8),
        font=dict(family="Archivo, Arial, sans-serif", size=13),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title_text=""),
        hoverlabel=dict(font_size=13),
    )
    return fig


def mostrar(fig):
    """Muestra el gráfico usando todo el ancho de su columna."""
    st.plotly_chart(fig, width="stretch", config=CONFIG_PLOTLY)


# -------------------------------------------------------------
# 3. Carga de datos
# -------------------------------------------------------------
RUTA_DATOS = "data/datos.csv"

try:
    df = cargar_datos(RUTA_DATOS)
except FileNotFoundError:
    st.error(
        f"No se encontró `{RUTA_DATOS}`. Crea una carpeta `data` junto a "
        "`app.py`, guarda ahí `datos.csv` y recarga la página."
    )
    st.stop()


# -------------------------------------------------------------
# 4. Título y subtítulo
# -------------------------------------------------------------
# El HTML va sin sangría: si se indenta 4 espacios, Streamlit lo muestra como código.
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bungee&family=Archivo:wght@400;600&display=swap');

.banner {
    background: #2B1055;
    border-radius: 14px;
    padding: 2rem 2.2rem 1.9rem;
    margin-bottom: 1.4rem;
}
.banner-titulo {
    font-family: 'Bungee', 'Arial Black', Impact, sans-serif;
    font-size: clamp(2rem, 5vw, 3.6rem);
    line-height: 1.1;
    color: #FFD23F;
    /* Doble sombra rosa y cian, como en los carteles de baile sonidero */
    text-shadow: 3px 3px 0 #FF2E88, 6px 6px 0 #00C2D1;
    margin-bottom: 1rem;
}
.banner-titulo .emoji {
    text-shadow: none;
}
.banner-subtitulo {
    font-family: 'Archivo', Arial, sans-serif;
    font-size: 1.12rem;
    line-height: 1.55;
    color: #EDE7F6;
    max-width: 62ch;
}
</style>
""",
    unsafe_allow_html=True,
)

anio_min = int(df["anio_lanzamiento"].min())
anio_max = int(df["anio_lanzamiento"].max())

st.markdown(
    f"""
<div class="banner">
<div class="banner-titulo"><span class="emoji">🎧</span> Hits de México en Spotify <span class="emoji">🔥</span></div>
<div class="banner-subtitulo">
🎶 {len(df)} canciones y {df["artista_principal"].nunique()} artistas que sonaron en México
entre {anio_min} y {anio_max}. Del reguetón a los corridos tumbados 🤠,
filtra y descubre quién manda en el país 🇲🇽
</div>
</div>
""",
    unsafe_allow_html=True,
)


# -------------------------------------------------------------
# 5. Filtros: dropdowns y checkboxes en la barra lateral
# -------------------------------------------------------------
st.sidebar.header("🎛️ Filtros")
st.sidebar.caption("Deja una lista vacía o en «Todos» para incluir todas las opciones.")

generos = st.sidebar.multiselect(
    "🎵 Género musical",
    sorted(df["genero_musical"].unique()),
    placeholder="Todos los géneros",
)

pais = st.sidebar.selectbox("🌎 País del artista", ["Todos"] + sorted(df["pais_artista"].unique()))

# Los artistas que se ofrecen dependen del género y del país elegidos
base_artistas = df
if generos:
    base_artistas = base_artistas[base_artistas["genero_musical"].isin(generos)]
if pais != "Todos":
    base_artistas = base_artistas[base_artistas["pais_artista"] == pais]
artista = st.sidebar.selectbox(
    "🎤 Artista principal", ["Todos"] + sorted(base_artistas["artista_principal"].unique())
)

sexo = st.sidebar.selectbox("👤 Sexo del artista", ["Todos"] + sorted(df["sexo_artista"].unique()))

rango_anios = st.sidebar.slider("📅 Años de lanzamiento", anio_min, anio_max, (anio_min, anio_max))

st.sidebar.subheader("✅ Mostrar solo canciones…")
solo_colaboraciones = st.sidebar.checkbox("🤝 Que son colaboraciones")
solo_origen_mx = st.sidebar.checkbox("🇲🇽 De artistas de origen mexicano")
solo_virales = st.sidebar.checkbox("📱 Virales en TikTok")
solo_numero_uno = st.sidebar.checkbox("🥇 Que llegaron al #1 en México")
sin_explicito = st.sidebar.checkbox("🚫 Sin contenido explícito")


# -------------------------------------------------------------
# 6. Aplicar filtros
# -------------------------------------------------------------
df_f = df.copy()
if generos:
    df_f = df_f[df_f["genero_musical"].isin(generos)]
if pais != "Todos":
    df_f = df_f[df_f["pais_artista"] == pais]
if artista != "Todos":
    df_f = df_f[df_f["artista_principal"] == artista]
if sexo != "Todos":
    df_f = df_f[df_f["sexo_artista"] == sexo]
df_f = df_f[df_f["anio_lanzamiento"].between(*rango_anios)]
if solo_colaboraciones:
    df_f = df_f[df_f["es_colaboracion"]]
if solo_origen_mx:
    df_f = df_f[df_f["origen_mexicano"]]
if solo_virales:
    df_f = df_f[df_f["viral_tiktok"]]
if solo_numero_uno:
    df_f = df_f[df_f["posicion_maxima_mx"] == 1]
if sin_explicito:
    df_f = df_f[~df_f["contenido_explicito"]]

if df_f.empty:
    st.warning(
        "Ninguna canción cumple todos los filtros. Desmarca alguna casilla, "
        "amplía el rango de años o vuelve a «Todos» en los menús de la barra lateral."
    )
    st.stop()


# -------------------------------------------------------------
# 7. Indicadores principales
# -------------------------------------------------------------
streams_mx = df_f["streams_mexico_millones"].sum()
streams_total = df_f["streams_totales_millones"].sum()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("🎵 Canciones", len(df_f), help=f"De un total de {len(df)} canciones.", border=True)
k2.metric("🎤 Artistas", df_f["artista_principal"].nunique(), border=True)
k3.metric("🇲🇽 Streams en México", f"{streams_mx:,.0f} M", border=True)
k4.metric(
    "📍 Peso de México",
    f"{streams_mx / streams_total:.0%}",
    help="Parte de los streams totales de estas canciones que vino de México.",
    border=True,
)
k5.metric("🥇 Llegaron al #1", int((df_f["posicion_maxima_mx"] == 1).sum()), border=True)


# -------------------------------------------------------------
# 8. Vista previa de los datos
# -------------------------------------------------------------
if st.checkbox("👀 Mostrar vista previa de los datos filtrados"):
    n_filas = st.slider("Filas a mostrar", 5, 10, 5)
    st.dataframe(
        df_f.head(n_filas),
        width="stretch",
        hide_index=True,
        column_config={
            "fecha_lanzamiento": st.column_config.DateColumn("fecha_lanzamiento", format="YYYY-MM-DD"),
            "anio_lanzamiento": st.column_config.NumberColumn("anio_lanzamiento", format="%d"),
            "bailabilidad": st.column_config.ProgressColumn("bailabilidad", min_value=0, max_value=1, format="%.2f"),
            "energia": st.column_config.ProgressColumn("energia", min_value=0, max_value=1, format="%.2f"),
            "streams_totales_millones": st.column_config.NumberColumn("streams_totales_millones", format="%.0f M"),
            "streams_mexico_millones": st.column_config.NumberColumn("streams_mexico_millones", format="%.1f M"),
            "porcentaje_streams_mexico": st.column_config.NumberColumn("porcentaje_streams_mexico", format="%d %%"),
        },
    )
    st.caption(
        f"Mostrando {min(n_filas, len(df_f))} de {len(df_f)} canciones. "
        "Haz clic en un encabezado para ordenar la tabla."
    )


# -------------------------------------------------------------
# 9. Gráficos 1 y 2, lado a lado
# -------------------------------------------------------------
col_izq, col_der = st.columns(2, gap="large")

METRICAS = {
    "Streams en México (M)": ("streams_mexico_millones", "sum"),
    "Streams totales (M)": ("streams_totales_millones", "sum"),
    "Número de canciones": ("id_cancion", "count"),
    "Semanas en el Top 50": ("semanas_top50_mx", "sum"),
}

# ---------- Gráfico 1: barras ----------
with col_izq:
    with st.container(border=True):
        st.subheader("📊 ¿Quién manda en México?")
        c1, c2 = st.columns(2)
        grupo = c1.selectbox(
            "Agrupar por",
            ["artista_principal", "genero_musical", "pais_artista", "anio_lanzamiento"],
            format_func=NOMBRES.get,
        )
        metrica = c2.selectbox("Medir", list(METRICAS))
        columna, funcion = METRICAS[metrica]

        if grupo == "anio_lanzamiento":
            # Barras verticales apiladas por género: muestran cómo cambia el gusto año con año
            resumen = (
                df_f.groupby(["anio_lanzamiento", "genero_musical"])
                .agg(valor=(columna, funcion))
                .reset_index()
            )
            fig = px.bar(
                resumen,
                x="anio_lanzamiento",
                y="valor",
                color="genero_musical",
                color_discrete_map=COLORES_GENERO,
                labels={"valor": metrica, "anio_lanzamiento": "Año", "genero_musical": "Género"},
            )
            fig.update_xaxes(dtick=1, title_text="")
            fig.update_layout(bargap=0.2)
        else:
            top_n = 10
            if grupo in ("artista_principal", "pais_artista"):
                top_n = st.slider("Mostrar los primeros", 5, 20, 10)

            resumen = (
                df_f.groupby(grupo)
                .agg(valor=(columna, funcion), canciones=("id_cancion", "count"))
                .reset_index()
                .sort_values("valor", ascending=False)
                .head(top_n)
            )
            etiquetas = {"valor": metrica, grupo: NOMBRES[grupo], "canciones": "Canciones"}

            if grupo == "genero_musical":
                # Cada género con su color fijo
                fig = px.bar(
                    resumen, x="valor", y=grupo, orientation="h",
                    color=grupo, color_discrete_map=COLORES_GENERO,
                    text_auto=",.0f", hover_data=["canciones"], labels=etiquetas,
                )
                fig.update_layout(showlegend=False)
            else:
                # Degradado: cuanto más alto el valor, más rosa la barra
                fig = px.bar(
                    resumen, x="valor", y=grupo, orientation="h",
                    color="valor", color_continuous_scale=ESCALA_CONTINUA,
                    text_auto=",.0f", hover_data=["canciones"], labels=etiquetas,
                )
                fig.update_coloraxes(showscale=False)

            fig.update_yaxes(categoryorder="total ascending", title_text="")
            fig.update_xaxes(title_text=metrica, range=[0, resumen["valor"].max() * 1.2])
            fig.update_traces(textposition="outside", cliponaxis=False)

        mostrar(dar_estilo(fig))

# ---------- Gráfico 2: dona o pastel ----------
with col_der:
    with st.container(border=True):
        st.subheader("🍩 ¿Cómo se reparte la escucha?")
        c1, c2 = st.columns(2)
        variable_pie = c1.selectbox(
            "Repartir por",
            ["genero_musical", "origen_mexicano", "sexo_artista", "tipo_artista",
             "es_colaboracion", "viral_tiktok", "contenido_explicito", "pais_artista"],
            format_func=NOMBRES.get,
        )
        medida_pie = c2.selectbox("Según", ["Streams en México (M)", "Número de canciones"])
        es_dona = st.checkbox("Mostrar como dona", value=True)

        datos_pie = df_f.assign(categoria=como_texto(df_f[variable_pie]))
        if medida_pie == "Número de canciones":
            resumen = datos_pie.groupby("categoria").size().reset_index(name="valor")
        else:
            resumen = (
                datos_pie.groupby("categoria")["streams_mexico_millones"]
                .sum()
                .reset_index(name="valor")
            )
        resumen = resumen.sort_values("valor", ascending=False)

        # Con más de 8 categorías (por ejemplo, países), juntamos las pequeñas en "Otros"
        if len(resumen) > 8:
            otros = pd.DataFrame({"categoria": ["Otros"], "valor": [resumen["valor"].iloc[7:].sum()]})
            resumen = pd.concat([resumen.head(7), otros])

        fig = px.pie(
            resumen,
            names="categoria",
            values="valor",
            color="categoria",
            color_discrete_map={**mapa_de_colores(variable_pie), "Otros": COLOR_OTROS},
            color_discrete_sequence=SECUENCIA,
            hole=0.55 if es_dona else 0,
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent",
            insidetextorientation="horizontal",
            sort=False,
            marker=dict(line=dict(color="rgba(255,255,255,0.9)", width=2)),
            hovertemplate="<b>%{label}</b><br>%{value:,.1f}<br>%{percent}<extra></extra>",
        )
        # Oculta los porcentajes que no caben en porciones muy pequeñas
        fig.update_layout(uniformtext_minsize=11, uniformtext_mode="hide")

        if es_dona:
            total = resumen["valor"].sum()
            unidad = "canciones" if medida_pie == "Número de canciones" else "M de streams"
            fig.add_annotation(text=f"<b>{total:,.0f}</b><br>{unidad}", showarrow=False, font=dict(size=20))

        mostrar(dar_estilo(fig))


# -------------------------------------------------------------
# 10. Gráfico 3: histograma a todo el ancho
# -------------------------------------------------------------
with st.container(border=True):
    st.subheader("📈 ¿Cómo suenan los hits?")
    c1, c2, c3 = st.columns([2, 2, 1.5])
    variable_hist = c1.selectbox(
        "Variable",
        ["porcentaje_streams_mexico", "bailabilidad", "energia", "bpm",
         "duracion_segundos", "semanas_top50_mx", "streams_totales_millones"],
        format_func=NOMBRES.get,
    )
    color_hist = c2.selectbox(
        "Colorear por",
        [None, "genero_musical", "origen_mexicano", "viral_tiktok", "es_colaboracion", "sexo_artista"],
        format_func=lambda c: "Un solo color" if c is None else NOMBRES[c],
    )
    n_bins = c3.slider("Número de barras", 5, 40, 20)

    c4, c5 = st.columns(2)
    marginal = c4.selectbox(
        "Gráfico de apoyo arriba",
        [None, "box", "violin", "rug"],
        format_func={None: "Ninguno", "box": "Caja", "violin": "Violín", "rug": "Marcas (rug)"}.get,
    )
    mostrar_media = c5.checkbox("Mostrar línea de la media", value=True)

    datos_hist = df_f.copy()
    if color_hist:
        datos_hist["grupo"] = como_texto(datos_hist[color_hist])

    fig = px.histogram(
        datos_hist,
        x=variable_hist,
        color="grupo" if color_hist else None,
        nbins=n_bins,
        marginal=marginal,
        color_discrete_map=mapa_de_colores(color_hist),
        color_discrete_sequence=SECUENCIA if color_hist else [MORADO],
        hover_data=["cancion", "artista_principal"],
        labels={variable_hist: NOMBRES[variable_hist], "grupo": NOMBRES.get(color_hist, "")},
        opacity=0.9,
    )
    fig.update_traces(
        marker_line_width=1,
        marker_line_color="rgba(255,255,255,0.8)",
        selector=dict(type="histogram"),
    )
    fig.update_yaxes(title_text="Número de canciones", row=1, col=1)

    media = df_f[variable_hist].mean()
    if mostrar_media:
        fig.add_vline(
            x=media, line_dash="dash", line_color=ROSA, line_width=2, row=1, col=1,
            annotation_text=f"Media: {media:,.2f}" if media < 10 else f"Media: {media:,.0f}",
            annotation_position="top right",
            annotation_font_color=ROSA,
        )

    mostrar(dar_estilo(fig, alto=470 if marginal else 400))
    st.caption(
        f"Mediana: {df_f[variable_hist].median():,.2f}. "
        "Pasa el cursor sobre las barras para ver cuántas canciones hay en cada rango; "
        "haz clic en la leyenda para ocultar o aislar un grupo."
    )


# -------------------------------------------------------------
# 11. Pie de página
# -------------------------------------------------------------
st.caption(
    "Fuente: data/datos.csv. Los streams, las posiciones y las características de audio "
    "son estimaciones."
)