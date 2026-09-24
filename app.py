import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
import os
from pathlib import Path

# ─────────────────────────────────────────────
#  CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Tierra de Gracia",
    page_icon="🥑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  ESTILOS CSS PERSONALIZADOS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;600&display=swap');

/* ── Fondo principal ── */
.stApp {
    background: linear-gradient(160deg, #0f1e0a 0%, #1a2f0f 50%, #0d1a08 100%);
    font-family: 'Lato', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1506 0%, #162208 60%, #1f3010 100%) !important;
    border-right: 1px solid #3d5c1a44;
}
[data-testid="stSidebar"] * {
    color: #d4c4a0 !important;
}

/* ── Encabezado sidebar ── */
.sidebar-header {
    text-align: center;
    padding: 1rem 0.5rem 1.5rem;
    border-bottom: 1px solid #4a7c2f33;
    margin-bottom: 1rem;
}
.sidebar-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #8fba4e !important;
    margin: 0.5rem 0 0.1rem;
    line-height: 1.2;
}
.sidebar-subtitle {
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: #c8a96e !important;
    text-transform: uppercase;
}

/* ── Tarjetas métricas ── */
.metric-card {
    background: linear-gradient(135deg, #1a2f0f 0%, #243d14 100%);
    border: 1px solid #4a7c2f55;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #4a7c2f, #c8a96e);
}
.metric-label {
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8fba4e;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #e8dcc0;
    line-height: 1;
}
.metric-delta {
    font-size: 0.78rem;
    color: #c8a96e;
    margin-top: 0.2rem;
}

/* ── Tarjetas de sección ── */
.section-card {
    background: linear-gradient(135deg, #162208 0%, #1f3010 100%);
    border: 1px solid #3d5c1a33;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #c8a96e;
    margin-bottom: 1rem;
    border-bottom: 1px solid #4a7c2f33;
    padding-bottom: 0.5rem;
}

/* ── Página title ── */
.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #8fba4e;
    margin-bottom: 0.2rem;
}
.page-subtitle {
    color: #c8a96e;
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* ── Inputs y selectboxes ── */
.stTextInput input, .stNumberInput input, .stTextArea textarea,
.stSelectbox select, .stDateInput input {
    background-color: #1a2f0f !important;
    border: 1px solid #4a7c2f66 !important;
    color: #e8dcc0 !important;
    border-radius: 8px !important;
}
.stTextInput label, .stNumberInput label, .stTextArea label,
.stSelectbox label, .stDateInput label {
    color: #a8c878 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.05em !important;
}

/* ── Botones ── */
.stButton > button {
    background: linear-gradient(135deg, #4a7c2f, #3d6626) !important;
    color: #e8dcc0 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    font-family: 'Lato', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #5a8f3a, #4a7c2f) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 15px #4a7c2f44 !important;
}

/* ── Tablas ── */
.stDataFrame, [data-testid="stDataFrame"] {
    border: 1px solid #3d5c1a44 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background-color: #162208 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: #8fba4e !important;
    border-radius: 7px !important;
    font-family: 'Lato', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #4a7c2f, #3d6626) !important;
    color: #e8dcc0 !important;
}

/* ── Success / info messages ── */
.stSuccess {
    background-color: #1a3a0e !important;
    border: 1px solid #4a7c2f !important;
    color: #8fba4e !important;
    border-radius: 8px !important;
}

/* ── Divider ── */
hr {
    border-color: #3d5c1a33 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f1e0a; }
::-webkit-scrollbar-thumb { background: #4a7c2f55; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CONEXIÓN A SUPABASE
# ─────────────────────────────────────────────
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")


def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase_client()

# ─────────────────────────────────────────────
#  FUNCIONES DE DATOS (Supabase)
# ─────────────────────────────────────────────
def cargar_plantas():
    res = supabase.table("plantas").select("*").order("id").execute()
    return res.data

def cargar_inversiones():
    res = supabase.table("inversiones").select("*").order("id").execute()
    return res.data

def cargar_tareas():
    res = supabase.table("tareas").select("*").order("id").execute()
    return res.data

def cargar_galeria():
    res = supabase.table("galeria").select("*").order("id").execute()
    return res.data

def insertar_planta(registro):
    supabase.table("plantas").insert(registro).execute()

def actualizar_planta(id, registro):
    supabase.table("plantas").update(registro).eq("id", id).execute()

def eliminar_planta(id):
    supabase.table("plantas").delete().eq("id", id).execute()    

def insertar_inversion(registro):
    supabase.table("inversiones").insert(registro).execute()

def actualizar_inversion(id, registro):
    supabase.table("inversiones").update(registro).eq("id", id).execute()

def eliminar_inversion(id):
    supabase.table("inversiones").delete().eq("id", id).execute()

def insertar_tarea(registro):
    supabase.table("tareas").insert(registro).execute()

def actualizar_tarea(id, registro):
    supabase.table("tareas").update(registro).eq("id", id).execute()

def eliminar_tarea(id):
    supabase.table("tareas").delete().eq("id", id).execute()

def insertar_galeria(registro):
    supabase.table("galeria").insert(registro).execute()

def eliminar_galeria_item(id):
    supabase.table("galeria").delete().eq("id", id).execute()
# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    # Logo e imagen
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("""
        <div class="sidebar-header">
            <div style="font-size:3rem;">🥑</div>
            <div class="sidebar-title">Tierra de<br>Gracia</div>
            <div class="sidebar-subtitle">Cultivo de Aguacates</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    pagina = st.radio(
        "Navegación",
        ["🌿 Dashboard", "🌱 Registro de Plantas", "💰 Inversiones & Gastos",
         "✅ Tareas & Actividades", "📷 Galería"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown(f"""
    <div style="text-align:center; color:#4a7c2f; font-size:0.7rem; letter-spacing:0.1em;">
        v1.0 · Venezuela 🇻🇪<br>
        <span style="color:#3d5c1a;">{datetime.now().strftime('%d/%m/%Y')}</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FUNCIÓN: LOGO HEADER
# ─────────────────────────────────────────────
def mostrar_logo_header(icono, titulo, subtitulo):
    col_logo, col_text = st.columns([1, 6])
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=70)
        else:
            st.markdown(f"<div style='font-size:2.5rem;padding-top:0.3rem'>{icono}</div>", unsafe_allow_html=True)
    with col_text:
        st.markdown(f"<div class='page-title'>{titulo}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='page-subtitle'>{subtitulo}</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  PÁGINA: DASHBOARD
# ═══════════════════════════════════════════════
if pagina == "🌿 Dashboard":
    mostrar_logo_header("🥑", "Tierra de Gracia", "Panel de Control · Cultivo de Aguacates")

    plantas = cargar_plantas()
    inversiones = cargar_inversiones()
    tareas = cargar_tareas()

    total_plantas = len(plantas)
    total_invertido = sum(float(i.get("monto", 0)) for i in inversiones)
    tareas_pendientes = len([t for t in tareas if t.get("estado") == "Pendiente"])
    plantas_vivas = len([p for p in plantas if p.get("estado") == "Viva"])

    # Métricas
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🌱 Total Plantas</div>
            <div class="metric-value">{total_plantas}</div>
            <div class="metric-delta">Registradas en el sistema</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💚 Plantas Vivas</div>
            <div class="metric-value">{plantas_vivas}</div>
            <div class="metric-delta">En buen estado</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💰 Total Invertido</div>
            <div class="metric-value">${total_invertido:,.0f}</div>
            <div class="metric-delta">Inversión acumulada</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">✅ Tareas Pendientes</div>
            <div class="metric-value">{tareas_pendientes}</div>
            <div class="metric-delta">Por completar</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.markdown('<div class="section-card"><div class="section-title">📊 Inversiones por Categoría</div>', unsafe_allow_html=True)
        if inversiones:
            df_inv = pd.DataFrame(inversiones)
            df_inv["monto"] = pd.to_numeric(df_inv["monto"], errors="coerce")
            resumen = df_inv.groupby("categoria")["monto"].sum().reset_index()
            fig = px.pie(resumen, values="monto", names="categoria",
                         color_discrete_sequence=["#4a7c2f","#8fba4e","#c8a96e","#a0785a","#6b9e3a","#d4b483"],
                         hole=0.45)
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#d4c4a0", showlegend=True,
                legend=dict(font=dict(color="#d4c4a0", size=11)),
                margin=dict(t=10, b=10, l=10, r=10), height=280
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Agrega inversiones para ver el gráfico.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_der:
        st.markdown('<div class="section-card"><div class="section-title">🌿 Estado de Plantas</div>', unsafe_allow_html=True)
        if plantas:
            estados = pd.DataFrame(plantas)["estado"].value_counts().reset_index()
            estados.columns = ["Estado", "Cantidad"]
            colores = {"Viva": "#4a7c2f", "En observación": "#c8a96e", "Muerta": "#8b2222"}
            fig2 = px.bar(estados, x="Estado", y="Cantidad",
                          color="Estado", color_discrete_map=colores,
                          text="Cantidad")
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#d4c4a0", showlegend=False,
                xaxis=dict(gridcolor="rgba(61,92,26,0.13)"),
                yaxis=dict(gridcolor="rgba(61,92,26,0.13)"),
                margin=dict(t=10, b=10, l=10, r=10), height=280
            )
            fig2.update_traces(textfont_color="#e8dcc0")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Agrega plantas para ver el gráfico.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Últimas tareas
    st.markdown('<div class="section-card"><div class="section-title">📋 Últimas Tareas</div>', unsafe_allow_html=True)
    if tareas:
        df_t = pd.DataFrame(tareas[-5:])
        st.dataframe(df_t[["titulo","categoria","prioridad","estado","fecha"]].rename(columns={
            "titulo":"Tarea","categoria":"Categoría","prioridad":"Prioridad","estado":"Estado","fecha":"Fecha"
        }), use_container_width=True, hide_index=True)
    else:        
        st.info("No hay tareas registradas aún.")
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  PÁGINA: REGISTRO DE PLANTAS
# ═══════════════════════════════════════════════
elif pagina == "🌱 Registro de Plantas":
    mostrar_logo_header("🌱", "Registro de Plantas", "Control y seguimiento por lotes de siembra")

    tab1, tab2 = st.tabs(["➕ Nuevo Lote", "📋 Mis Lotes"])

    with tab1:
        st.markdown('<div class="section-card"><div class="section-title">Registrar Nuevo Lote</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            numero_lote = st.text_input("Número de Lote", placeholder="Ej: Lote-01")
            cantidad_matas = st.number_input("Cantidad de Matas", min_value=1, step=1)
            fecha_siembra = st.date_input("Fecha de siembra", value=date.today())
        with c2:
            variedad = st.selectbox("Variedad", ["Choquette", "Hass", "Criollo"])
            zona = st.text_input("Zona / Parcela", placeholder="Ej: Zona Norte")
            estado = st.selectbox("Estado actual", ["Viva", "En observación", "Muerta"])
        with c3:
            origen = st.selectbox("Origen de la planta", ["Semilla propia", "Vivero", "Injerto", "Otro"])
            riego = st.selectbox("Tipo de riego", ["Goteo", "Aspersión", "Manual", "Lluvia"])
            notas = st.text_area("Notas", placeholder="Observaciones adicionales...", height=100)

            if st.button("💾 Guardar Lote"):
                if numero_lote and cantidad_matas > 0:
                    nuevo_lote = {
                        "lote": numero_lote,
                        "cantidad_matas": cantidad_matas,
                        "variedad": variedad,
                        "fecha_siembra": str(fecha_siembra),
                        "zona": zona,
                        "estado": estado,
                        "origen": origen,
                        "riego": riego,
                        "notas": notas,
                        "fecha_registro": str(date.today())
                    }
                    insertar_planta(nuevo_lote)
                    st.success(f"✅ {numero_lote} registrado con {cantidad_matas} matas.")
                else:
                    st.error("El número de lote y la cantidad de matas son obligatorios.")

            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-card"><div class="section-title">Listado de Lotes</div>', unsafe_allow_html=True)
        plantas_data = cargar_plantas()
        if plantas_data:
            df_p = pd.DataFrame(plantas_data)
            if "cantidad_matas" not in df_p.columns:
                df_p["cantidad_matas"] = 1
            if "lote" not in df_p.columns:
                df_p["lote"] = df_p.get("id", "—")

            filtro = st.selectbox("Filtrar por estado", ["Todos", "Viva", "En observación", "Muerta"])
            df_filtrado = df_p if filtro == "Todos" else df_p[df_p["estado"] == filtro]

            total_matas = pd.to_numeric(df_filtrado["cantidad_matas"], errors="coerce").fillna(0).astype(int).sum()
            total_lotes = len(df_filtrado)
            m1, m2 = st.columns(2)
            m1.metric("🌱 Total Lotes", total_lotes)
            m2.metric("🥑 Total Matas", total_matas)

            st.dataframe(df_filtrado[["lote","cantidad_matas","variedad","fecha_siembra","zona","estado","riego","notas"]].rename(columns={
                "lote": "Lote", "cantidad_matas": "Matas", "variedad": "Variedad",
                "fecha_siembra": "Fecha Siembra", "zona": "Zona", "estado": "Estado",
                "riego": "Riego", "notas": "Notas"
            }), use_container_width=True, hide_index=True)

            st.caption(f"Mostrando {total_lotes} lote(s) · {total_matas} matas en total")

            # ── Editar o eliminar ──
            st.markdown("---")
            with st.expander("✏️ Editar o eliminar un lote"):
                opciones = {f"{row['lote']} (id {row['id']})": row for _, row in df_p.iterrows()}
                seleccion = st.selectbox("Selecciona el lote", list(opciones.keys()))
                registro = opciones[seleccion]
                reg_id = registro["id"]

                ec1, ec2, ec3 = st.columns(3)
                with ec1:
                    e_lote = st.text_input("Número de Lote", value=registro.get("lote",""), key="e_lote")
                    e_matas = st.number_input("Cantidad de Matas", min_value=1, step=1, value=int(registro.get("cantidad_matas",1)), key="e_matas")
                    e_fecha = st.text_input("Fecha de siembra", value=str(registro.get("fecha_siembra","")), key="e_fecha")
                with ec2:
                    variedades = ["Choquette", "Hass", "Criollo"]
                    e_variedad = st.selectbox("Variedad", variedades, index=variedades.index(registro.get("variedad","Hass")) if registro.get("variedad") in variedades else 0, key="e_variedad")
                    e_zona = st.text_input("Zona / Parcela", value=registro.get("zona",""), key="e_zona")
                    estados = ["Viva", "En observación", "Muerta"]
                    e_estado = st.selectbox("Estado actual", estados, index=estados.index(registro.get("estado","Viva")) if registro.get("estado") in estados else 0, key="e_estado")
                with ec3:
                    origenes = ["Semilla propia", "Vivero", "Injerto", "Otro"]
                    e_origen = st.selectbox("Origen", origenes, index=origenes.index(registro.get("origen","Vivero")) if registro.get("origen") in origenes else 0, key="e_origen")
                    riegos = ["Goteo", "Aspersión", "Manual", "Lluvia"]
                    e_riego = st.selectbox("Tipo de riego", riegos, index=riegos.index(registro.get("riego","Goteo")) if registro.get("riego") in riegos else 0, key="e_riego")
                    e_notas = st.text_area("Notas", value=registro.get("notas",""), key="e_notas")

                bc1, bc2 = st.columns(2)
                with bc1:
                    if st.button("💾 Guardar cambios", key="btn_edit_planta"):
                        actualizar_planta(reg_id, {
                            "lote": e_lote, "cantidad_matas": e_matas, "variedad": e_variedad,
                            "fecha_siembra": e_fecha, "zona": e_zona, "estado": e_estado,
                            "origen": e_origen, "riego": e_riego, "notas": e_notas
                        })
                        st.success("✅ Lote actualizado.")
                        st.rerun()
                with bc2:
                    if st.button("🗑️ Eliminar lote", key="btn_del_planta"):
                        eliminar_planta(reg_id)
                        st.success("🗑️ Lote eliminado.")
                        st.rerun()
        else:
            st.info("Aún no hay lotes registrados. ¡Agrega el primero!")
        st.markdown('</div>', unsafe_allow_html=True)
    
# ═══════════════════════════════════════════════
#  PÁGINA: INVERSIONES & GASTOS
# ═══════════════════════════════════════════════
elif pagina == "💰 Inversiones & Gastos":
    mostrar_logo_header("💰", "Inversiones & Gastos", "Control financiero del proyecto")

    tab1, tab2 = st.tabs(["➕ Nueva Inversión", "📊 Historial"])

    with tab1:
        st.markdown('<div class="section-card"><div class="section-title">Registrar Gasto / Inversión</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            descripcion = st.text_input("Descripción", placeholder="Ej: Compra de plantas Hass")
            categoria = st.selectbox("Categoría", [
                "Siembra", "Fertilizante", "Riego", "Herramientas",
                "Mano de obra", "Cercado", "Transporte", "Otro"
            ])
        with c2:
            monto = st.number_input("Monto ($)", min_value=0.0, step=0.50)
            metodo = st.selectbox("Método de pago", ["Efectivo", "Transferencia", "Tarjeta", "Otro"])
        with c3:
            fecha_inv = st.date_input("Fecha", value=date.today())
            proyecto = st.text_input("Proyecto / Partida", placeholder="Ej: Siembra de Aguacates")
            notas_inv = st.text_area("Notas", height=80)

        if st.button("💾 Guardar Inversión"):
                if descripcion and monto > 0:
                    nueva_inv = {
                        "descripcion": descripcion, "categoria": categoria,
                        "monto": monto, "metodo": metodo,
                        "fecha": str(fecha_inv), "proyecto": proyecto, "notas": notas_inv
                    }
                    insertar_inversion(nueva_inv)
                    st.success(f"✅ Gasto de ${monto:,.2f} registrado.")
                else:
                    st.error("Completa la descripción y el monto.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-card"><div class="section-title">Historial de Inversiones</div>', unsafe_allow_html=True)
        inversiones_data = cargar_inversiones()
        if inversiones_data:
            df_inv = pd.DataFrame(inversiones_data)
            df_inv["monto"] = pd.to_numeric(df_inv["monto"])

            total = df_inv["monto"].sum()
            st.markdown(f"""
            <div class="metric-card" style="max-width:300px">
                <div class="metric-label">💰 Total Invertido</div>
                <div class="metric-value">${total:,.2f}</div>
            </div>""", unsafe_allow_html=True)

            df_inv["fecha"] = pd.to_datetime(df_inv["fecha"])
            df_inv_sorted = df_inv.sort_values("fecha")
            df_inv_sorted["acumulado"] = df_inv_sorted["monto"].cumsum()
            fig = px.area(df_inv_sorted, x="fecha", y="acumulado",
                          color_discrete_sequence=["#4a7c2f"],
                          labels={"fecha":"Fecha","acumulado":"Inversión Acumulada ($)"})
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#d4c4a0",
                xaxis=dict(gridcolor="rgba(61,92,26,0.13)"),
                yaxis=dict(gridcolor="rgba(61,92,26,0.13)"),
                margin=dict(t=10,b=10,l=10,r=10), height=220
            )
            fig.update_traces(fillcolor="rgba(74,124,47,0.2)", line_color="#8fba4e")
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(df_inv.rename(columns={
                "descripcion":"Descripción","categoria":"Categoría",
                "monto":"Monto ($)","metodo":"Pago","fecha":"Fecha",
                "proyecto":"Proyecto","notas":"Notas"
            }), use_container_width=True, hide_index=True)

            st.markdown("---")
            with st.expander("✏️ Editar o eliminar una inversión"):
                df_raw = pd.DataFrame(inversiones_data)
                opciones = {f"{row['descripcion']} - ${float(row['monto']):,.2f} (id {row['id']})": row for _, row in df_raw.iterrows()}
                seleccion = st.selectbox("Selecciona la inversión", list(opciones.keys()))
                registro = opciones[seleccion]
                reg_id = registro["id"]

                ec1, ec2, ec3 = st.columns(3)
                with ec1:
                    e_desc = st.text_input("Descripción", value=registro.get("descripcion",""), key="e_desc")
                    categorias = ["Siembra", "Fertilizante", "Riego", "Herramientas", "Mano de obra", "Cercado", "Transporte", "Otro"]
                    e_cat = st.selectbox("Categoría", categorias, index=categorias.index(registro.get("categoria","Otro")) if registro.get("categoria") in categorias else 0, key="e_cat")
                with ec2:
                    e_monto = st.number_input("Monto ($)", min_value=0.0, step=0.50, value=float(registro.get("monto",0)), key="e_monto")
                    metodos = ["Efectivo", "Transferencia", "Tarjeta", "Otro"]
                    e_metodo = st.selectbox("Método de pago", metodos, index=metodos.index(registro.get("metodo","Efectivo")) if registro.get("metodo") in metodos else 0, key="e_metodo")
                with ec3:
                    e_fecha = st.text_input("Fecha", value=str(registro.get("fecha","")), key="e_fecha_inv")
                    e_proyecto = st.text_input("Proyecto / Partida", value=registro.get("proyecto",""), key="e_proyecto")
                    e_notas = st.text_area("Notas", value=registro.get("notas",""), key="e_notas_inv")

                bc1, bc2 = st.columns(2)
                with bc1:
                    if st.button("💾 Guardar cambios", key="btn_edit_inv"):
                        actualizar_inversion(reg_id, {
                            "descripcion": e_desc, "categoria": e_cat, "monto": e_monto,
                            "metodo": e_metodo, "fecha": e_fecha, "proyecto": e_proyecto, "notas": e_notas
                        })
                        st.success("✅ Inversión actualizada.")
                        st.rerun()
                with bc2:
                    if st.button("🗑️ Eliminar inversión", key="btn_del_inv"):
                        eliminar_inversion(reg_id)
                        st.success("🗑️ Inversión eliminada.")
                        st.rerun()
        else:
            st.info("No hay inversiones registradas aún.")
        st.markdown('</div>', unsafe_allow_html=True)
# ═══════════════════════════════════════════════
#  PÁGINA: TAREAS & ACTIVIDADES
# ═══════════════════════════════════════════════
elif pagina == "✅ Tareas & Actividades":
    mostrar_logo_header("✅", "Tareas & Actividades", "Gestión de labores del cultivo")

    tab1, tab2 = st.tabs(["➕ Nueva Tarea", "📋 Lista de Tareas"])

    with tab1:
        st.markdown('<div class="section-card"><div class="section-title">Crear Nueva Tarea</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            titulo_t = st.text_input("Título de la tarea", placeholder="Ej: Aplicar fertilizante Zona Norte")
            categoria_t = st.selectbox("Categoría", [
                "Riego", "Fertilización", "Poda", "Control de plagas",
                "Siembra", "Cosecha", "Mantenimiento", "Otro"
            ])
            prioridad_t = st.selectbox("Prioridad", ["Alta", "Media", "Baja"])
        with c2:
            fecha_t = st.date_input("Fecha límite", value=date.today())
            asignado_t = st.selectbox("Asignado a", ["Yo", "Hermano", "Ambos", "Trabajador"])
            estado_t = st.selectbox("Estado", ["Pendiente", "En progreso", "Completada"])
        desc_t = st.text_area("Descripción detallada", placeholder="Detalles de la tarea...", height=100)

        if st.button("💾 Guardar Tarea"):
            if titulo_t:
                nueva_t = {
                    "titulo": titulo_t, "categoria": categoria_t,
                    "prioridad": prioridad_t, "fecha": str(fecha_t),
                    "asignado": asignado_t, "estado": estado_t,
                    "descripcion": desc_t,
                    "fecha_creacion": str(date.today())
                }
                insertar_tarea(nueva_t)
                st.success("✅ Tarea guardada correctamente.")
            else:
                st.error("El título es obligatorio.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-card"><div class="section-title">Lista de Tareas</div>', unsafe_allow_html=True)
        tareas_data = cargar_tareas()
        if tareas_data:
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                filtro_est = st.selectbox("Filtrar por estado", ["Todos","Pendiente","En progreso","Completada"])
            with c_f2:
                filtro_pri = st.selectbox("Filtrar por prioridad", ["Todos","Alta","Media","Baja"])

            df_t = pd.DataFrame(tareas_data)

            df_t_filtrado = df_t.copy()
            if filtro_est != "Todos":
                df_t_filtrado = df_t_filtrado[df_t_filtrado["estado"] == filtro_est]
            if filtro_pri != "Todos":
                df_t_filtrado = df_t_filtrado[df_t_filtrado["prioridad"] == filtro_pri]

            pendientes = len([t for t in tareas_data if t["estado"] == "Pendiente"])
            completadas = len([t for t in tareas_data if t["estado"] == "Completada"])

            m1, m2, m3 = st.columns(3)
            m1.metric("Total", len(tareas_data))
            m2.metric("Pendientes", pendientes)
            m3.metric("Completadas", completadas)

            st.dataframe(df_t_filtrado.rename(columns={
                "titulo":"Tarea","categoria":"Categoría","prioridad":"Prioridad",
                "fecha":"Fecha límite","asignado":"Asignado","estado":"Estado"
            })[["Tarea","Categoría","Prioridad","Fecha límite","Asignado","Estado"]],
            use_container_width=True, hide_index=True)

            st.markdown("---")
            with st.expander("✏️ Editar o eliminar una tarea"):
                opciones = {f"{row['titulo']} (id {row['id']})": row for _, row in df_t.iterrows()}
                seleccion = st.selectbox("Selecciona la tarea", list(opciones.keys()))
                registro = opciones[seleccion]
                reg_id = registro["id"]

                ec1, ec2 = st.columns(2)
                with ec1:
                    e_titulo = st.text_input("Título", value=registro.get("titulo",""), key="e_titulo")
                    categorias = ["Riego", "Fertilización", "Poda", "Control de plagas", "Siembra", "Cosecha", "Mantenimiento", "Otro"]
                    e_cat = st.selectbox("Categoría", categorias, index=categorias.index(registro.get("categoria","Otro")) if registro.get("categoria") in categorias else 0, key="e_cat_t")
                    prioridades = ["Alta", "Media", "Baja"]
                    e_prioridad = st.selectbox("Prioridad", prioridades, index=prioridades.index(registro.get("prioridad","Media")) if registro.get("prioridad") in prioridades else 0, key="e_prioridad")
                with ec2:
                    e_fecha = st.text_input("Fecha límite", value=str(registro.get("fecha","")), key="e_fecha_t")
                    asignados = ["Yo", "Hermano", "Ambos", "Trabajador"]
                    e_asignado = st.selectbox("Asignado a", asignados, index=asignados.index(registro.get("asignado","Yo")) if registro.get("asignado") in asignados else 0, key="e_asignado")
                    estados = ["Pendiente", "En progreso", "Completada"]
                    e_estado = st.selectbox("Estado", estados, index=estados.index(registro.get("estado","Pendiente")) if registro.get("estado") in estados else 0, key="e_estado_t")
                e_desc = st.text_area("Descripción", value=registro.get("descripcion",""), key="e_desc_t")

                bc1, bc2 = st.columns(2)
                with bc1:
                    if st.button("💾 Guardar cambios", key="btn_edit_tarea"):
                        actualizar_tarea(reg_id, {
                            "titulo": e_titulo, "categoria": e_cat, "prioridad": e_prioridad,
                            "fecha": e_fecha, "asignado": e_asignado, "estado": e_estado, "descripcion": e_desc
                        })
                        st.success("✅ Tarea actualizada.")
                        st.rerun()
                with bc2:
                    if st.button("🗑️ Eliminar tarea", key="btn_del_tarea"):
                        eliminar_tarea(reg_id)
                        st.success("🗑️ Tarea eliminada.")
                        st.rerun()
        else:
            st.info("No hay tareas registradas aún.")
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  PÁGINA: GALERÍA
# ═══════════════════════════════════════════════
elif pagina == "📷 Galería":
    mostrar_logo_header("📷", "Galería", "Fotos y registro visual del cultivo")

    st.markdown('<div class="section-card"><div class="section-title">Subir Fotos</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        titulo_foto = st.text_input("Título de la foto", placeholder="Ej: Zona Norte - Mayo 2026")
        categoria_foto = st.selectbox("Categoría", ["General","Plantas","Zona","Problema","Progreso","Cosecha"])
    with c2:
        fecha_foto = st.date_input("Fecha de la foto", value=date.today())
        notas_foto = st.text_area("Notas", height=80)

    foto = st.file_uploader("Selecciona una imagen", type=["jpg","jpeg","png","webp"])

    if st.button("📤 Subir Foto") and foto:
        nombre_archivo = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{foto.name}"
        contenido = foto.getbuffer().tobytes()

        supabase.storage.from_("galeria").upload(
            nombre_archivo, contenido,
            {"content-type": foto.type}
        )
        url_publica = supabase.storage.from_("galeria").get_public_url(nombre_archivo)

        insertar_galeria({
            "titulo": titulo_foto, "categoria": categoria_foto,
            "fecha": str(fecha_foto), "notas": notas_foto,
            "archivo_url": url_publica
        })
        st.success("✅ Foto guardada en la galería.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Mostrar galería
    st.markdown('<div class="section-card"><div class="section-title">📸 Fotos del Proyecto</div>', unsafe_allow_html=True)
    fotos_guardadas = cargar_galeria()

    if fotos_guardadas:
        filtro_cat = st.selectbox("Filtrar categoría", ["Todas","General","Plantas","Zona","Problema","Progreso","Cosecha"])
        fotos_filtradas = fotos_guardadas if filtro_cat == "Todas" else [f for f in fotos_guardadas if f.get("categoria") == filtro_cat]

        cols = st.columns(3)
        for i, foto_data in enumerate(reversed(fotos_filtradas)):
            url = foto_data.get("archivo_url", "")
            if url:
                with cols[i % 3]:
                    st.image(url, use_container_width=True)
                    st.markdown(f"""
                    <div style="color:#c8a96e;font-size:0.8rem;font-weight:600;">{foto_data.get('titulo','Sin título')}</div>
                    <div style="color:#8fba4e;font-size:0.7rem;">{foto_data.get('categoria','')} · {foto_data.get('fecha','')}</div>
                    """, unsafe_allow_html=True)
                    if st.button("🗑️ Eliminar", key=f"del_foto_{foto_data['id']}"):
                        eliminar_galeria_item(foto_data['id'])
                        st.success("🗑️ Foto eliminada.")
                        st.rerun()
    else:
        st.info("Sube la primera foto de tu cultivo.")
    st.markdown('</div>', unsafe_allow_html=True)
