# 🎧 Hits de México en Spotify (2015–2025)

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Datos-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly_Express-Gráficos-3F4F75?logo=plotly&logoColor=white)

> 🎶 **Del reguetón a los corridos tumbados: una década de música contada con datos.**

**Hits de México en Spotify** es una aplicación web interactiva que analiza **150 canciones** de **81 artistas** de **15 países** que marcaron la escucha en México entre 2015 y 2025.

Con unos pocos clics puedes descubrir:
- 🎤 qué artistas dominan el país;
- 🤠 cómo los corridos tumbados y el regional mexicano pasaron de nicho a protagonistas;
- 🌎 qué géneros dependen del público mexicano y cuáles triunfan en todo el mundo.

El proyecto muestra un flujo completo de análisis: limpieza y tipado de datos con **Pandas**, filtros que recalculan todo al instante, y visualizaciones interactivas con **Plotly Express**, publicadas en una interfaz construida con **Streamlit**.

<!-- 📸 Agrega aquí una captura del panel y quita los símbolos de comentario:
![Vista del panel](assets/captura_panel.png)
-->

---

## ✨ Características principales

1. **🎛️ Filtros en la barra lateral**
   - Menús desplegables: género, país, artista, sexo del artista y rango de años.
   - Casillas para quedarte solo con colaboraciones, artistas de origen mexicano, virales en TikTok, canciones que llegaron al #1 o sin contenido explícito.
2. **📌 Indicadores clave:** canciones, artistas, streams en México, peso de México en la escucha total y número de canciones que llegaron al #1.
3. **👀 Vista previa de los datos** que puedes mostrar u ocultar, con entre 5 y 10 filas ordenables.
4. **📊 Ranking en barras** por artista, género, país o año. La vista por año apila los géneros para ver cómo cambia el gusto musical.
5. **🍩 Gráfico de dona o pastel** para ver cómo se reparte la escucha por género, origen, tipo de artista, colaboración o viralidad.
6. **📈 Histograma** de bailabilidad, energía, tempo, duración y más. Puedes añadir arriba un gráfico de caja, violín o marcas, y una línea con la media.
7. **🎨 Diseño cuidado:** cada género conserva su color en todos los gráficos, y la app se adapta al modo claro y al modo oscuro.

> 💡 **Dato para explorar:** agrupa el gráfico de barras por **año** y observa cómo crece el bloque rosa de los corridos tumbados a partir de 2022.

---

## 🚀 Instalación en local

> ✅ **Requisitos previos:** tener instalados [Python 3.10 o superior](https://www.python.org/downloads/) y [Git](https://git-scm.com/downloads).

1. **Clona el repositorio** y entra en la carpeta del proyecto:

   ```bash
   git clone https://github.com/TU_USUARIO/top_20_mexico_spotify.git
   cd top_20_mexico_spotify
   ```

2. **Crea un ambiente virtual** para que las librerías del proyecto no se mezclen con las de tu sistema:

   ```bash
   python -m venv .venv
   ```

3. **Activa el ambiente virtual** según tu terminal:

   | Terminal | Comando |
   |---|---|
   | Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
   | Windows (Git Bash) | `source .venv/Scripts/activate` |
   | macOS / Linux | `source .venv/bin/activate` |

   Sabrás que funcionó porque verás `(.venv)` al inicio de la línea de la terminal.

4. **Instala las dependencias** listadas en `requirements.txt`:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. **Inicia la aplicación:**

   ```bash
   python -m streamlit run app.py
   ```

6. **Abre tu navegador** en [http://localhost:8501](http://localhost:8501). Si no se abre solo, copia esa dirección. ¡Listo para explorar! 🎉

> 🛠️ **¿Ves `ModuleNotFoundError`?** Casi siempre significa que el ambiente virtual no está activo. Repite el paso 3, confirma que aparece `(.venv)` y vuelve a ejecutar los pasos 4 y 5.

---

## 🗂️ Estructura del proyecto

```
top_20_mexico_spotify/
├── data/
│   └── datos.csv          # Conjunto de datos: 150 canciones, 23 columnas
├── app.py                 # Aplicación de Streamlit
├── requirements.txt       # Dependencias del proyecto
├── .gitignore
└── README.md
```

---

## 📊 Sobre los datos

El archivo `data/datos.csv` reúne **150 canciones lanzadas entre 2015 y 2025** y describe cada una con 23 columnas:

- **Categóricas:** artista, invitados, país, tipo y sexo del artista, género musical.
- **Numéricas:** duración, BPM, bailabilidad, energía, streams totales, streams en México, posición máxima y semanas en el Top 50.
- **Fecha:** fecha y año de lanzamiento.
- **Booleanas:** colaboración, contenido explícito, origen mexicano y viralidad en TikTok.

> ⚠️ **Nota de transparencia:** las canciones, los artistas y los años de lanzamiento son reales. Los streams, las posiciones en listas y las características de audio son **estimaciones con fines de análisis y demostración**, no cifras oficiales de Spotify.

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso en el proyecto |
|---|---|
| 🐍 **Python 3.12** | Lenguaje principal del análisis y de la aplicación |
| 🐼 **Pandas** | Carga, limpieza, tipado y agregación de los datos |
| 📈 **Plotly Express** | Gráficos interactivos: barras, dona o pastel e histograma |
| 🎈 **Streamlit** | Interfaz web, filtros, indicadores y tabla interactiva |
| 🌿 **Git y GitHub** | Control de versiones y publicación del proyecto |

---

## 👤 Autor

**TU NOMBRE**: analista de datos en formación, apasionado por contar historias con datos 🎵📊

- 💼 LinkedIn: [linkedin.com/in/TU_PERFIL](https://www.linkedin.com/in/TU_PERFIL)
- 🐙 GitHub: [github.com/TU_USUARIO](https://github.com/TU_USUARIO)

> ⭐ **¿Te gustó el proyecto?** Dale una estrella al repositorio y compártelo. ¡Tus comentarios y sugerencias son bienvenidos!
