
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (
    Rectangle, Circle, FancyArrowPatch, FancyBboxPatch
)
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation

# ==========================================================
# SIMULASI GAYA LORENTZ V12
# POROS TETAP DIAM, KUMPARAN OVAL BERPUTAR MENGELILINGI POROS
# ==========================================================

# PARAMETER AWAL
B_AWAL = 0.5
I_AWAL = 2.0

PANJANG = 0.12
JUMLAH_LILITAN = 1
LUAS_LILITAN = 0.0015

SUDUT_GAYA_AWAL = 90
SUDUT_TORSI_AWAL = 90

B = B_AWAL
I = I_AWAL

sudut_gaya = SUDUT_GAYA_AWAL
sudut_torsi = SUDUT_TORSI_AWAL

arah_arus = 1
berjalan = True
waktu = 0.0

DT = 0.04

# Ukuran kumparan
LEBAR = 1.75
TINGGI = 1.15
JUMLAH_TITIK_OVAL = 240

# Proyeksi visual 3D
FAKTOR_X = 0.42
FAKTOR_Y = 0.90
FAKTOR_KEDALAMAN = 0.18

# WARNA
BG = "#031329"
PANEL = "#0A2042"
BLUE = "#087CFF"
CYAN = "#00C8FF"
ORANGE = "#FF922E"
COPPER = "#C87535"
RED = "#FF315E"
GREEN = "#00E78B"
WHITE = "#F4F7FF"
YELLOW = "#FFE044"
GREY = "#A8B8D8"

plt.rcParams["font.family"] = "DejaVu Sans"

# ==========================================================
# FUNGSI PROYEKSI 3D KE LAYAR
# ==========================================================

def proyeksi_3d(x, y, z):
    layar_x = x + FAKTOR_X * y
    layar_y = FAKTOR_Y * z - FAKTOR_KEDALAMAN * y
    return layar_x, layar_y


# ==========================================================
# JENDELA UTAMA
# ==========================================================

fig = plt.figure(figsize=(15, 9), facecolor=BG)

try:
    fig.canvas.manager.set_window_title(
        "SIMULASI GAYA LORENTZ V12"
    )
except Exception:
    pass

fig.text(
    0.5, 0.965,
    "SIMULASI GAYA LORENTZ V12",
    ha="center", fontsize=23,
    color=WHITE, weight="bold"
)

fig.text(
    0.5, 0.925,
    "PHYSICS ENGINEERING | ROTATING COIL MOTOR",
    ha="center", fontsize=10,
    color=CYAN, weight="bold"
)

fig.add_artist(plt.Line2D(
    [0.035, 0.965],
    [0.895, 0.895],
    color=BLUE, linewidth=1.5
))

# ==========================================================
# AREA VISUALISASI
# ==========================================================

ax = fig.add_axes([0.025, 0.265, 0.68, 0.61])

ax.set_facecolor(BG)
ax.set_xlim(-5, 5)
ax.set_ylim(-3.5, 3.5)
ax.set_aspect("equal")
ax.axis("off")

ax.add_patch(FancyBboxPatch(
    (-4.95, -3.4),
    9.9, 6.8,
    boxstyle="round,pad=0.10",
    facecolor=PANEL,
    edgecolor=BLUE,
    linewidth=1.5,
    zorder=-10
))

ax.text(
    0, 3.05,
    "VISUALISASI MOTOR KAWAT BERARUS",
    ha="center", fontsize=12,
    color=CYAN, weight="bold"
)

# ==========================================================
# MEDAN MAGNET
# ==========================================================

simbol_magnet = []

for xx in np.linspace(-1.7, 1.7, 7):
    for yy in np.linspace(-1.1, 1.1, 5):
        simbol, = ax.plot(
            xx, yy,
            marker="x",
            color=BLUE,
            markersize=8,
            markeredgewidth=2,
            alpha=0.7,
            zorder=2
        )
        simbol_magnet.append(simbol)

panah_magnet = []

for yy in np.linspace(-1.15, 1.15, 5):
    panah = FancyArrowPatch(
        (-2.75, yy),
        (2.65, yy),
        arrowstyle="-|>",
        mutation_scale=13,
        color=CYAN,
        linewidth=1.3,
        alpha=0.6,
        zorder=3
    )
    ax.add_patch(panah)
    panah_magnet.append(panah)

ax.text(
    0, 1.75,
    "MEDAN MAGNET (B) : N → S",
    ha="center", fontsize=10,
    color=CYAN, weight="bold"
)

# ==========================================================
# MAGNET N DAN S
# ==========================================================

ax.add_patch(FancyBboxPatch(
    (-4.1, -1.5),
    1.1, 3,
    boxstyle="round,pad=0.08",
    facecolor="#D92346",
    edgecolor=RED,
    linewidth=2,
    zorder=4
))

ax.text(
    -3.55, 0, "N",
    ha="center", va="center",
    fontsize=32, color=WHITE,
    weight="bold"
)

ax.add_patch(FancyBboxPatch(
    (3.0, -1.5),
    1.1, 3,
    boxstyle="round,pad=0.08",
    facecolor="#0759E9",
    edgecolor=CYAN,
    linewidth=2,
    zorder=4
))

ax.text(
    3.55, 0, "S",
    ha="center", va="center",
    fontsize=32, color=WHITE,
    weight="bold"
)

# ==========================================================
# MEJA DAN PENYANGGA
# ==========================================================

ax.add_patch(Rectangle(
    (-2.8, -2.95),
    5.6, 0.38,
    facecolor="#754324",
    edgecolor="#BD8049",
    linewidth=1.5,
    zorder=4
))

for px in (-2.35, 2.35):
    ax.add_patch(Rectangle(
        (px - 0.18, -0.28),
        0.36, 0.56,
        facecolor="#8C9DB5",
        edgecolor=WHITE,
        linewidth=1.2,
        zorder=5
    ))

# ==========================================================
# POROS KAWAT LURUS HORIZONTAL
# BAGIAN INI TIDAK PERNAH DIANIMASIKAN
# ==========================================================

poros, = ax.plot(
    [-2.85, 2.85],
    [0, 0],
    color=COPPER,
    linewidth=9,
    solid_capstyle="round",
    zorder=13
)

poros_cahaya, = ax.plot(
    [-2.85, 2.85],
    [0.045, 0.045],
    color="#FFD18A",
    linewidth=1.8,
    zorder=14
)

ax.add_patch(Circle(
    (-2.85, 0), 0.105,
    facecolor="#FFD18A",
    edgecolor=WHITE,
    linewidth=1,
    zorder=15
))

ax.add_patch(Circle(
    (2.85, 0), 0.105,
    facecolor="#FFD18A",
    edgecolor=WHITE,
    linewidth=1,
    zorder=15
))

ax.text(
    0, -0.38,
    "POROS KAWAT LURUS (TETAP)",
    ha="center", fontsize=8,
    color="#FFD18A", weight="bold"
)

# ==========================================================
# KUMPARAN OVAL YANG MENGELILINGI POROS
#
# Kumparan berada pada bidang Y-Z.
# Poros berada pada arah X.
# Hanya koordinat kumparan yang berubah saat animasi.
# ==========================================================

sudut_oval = np.linspace(
    0, 2 * np.pi,
    JUMLAH_TITIK_OVAL,
    endpoint=False
)

radius_horizontal = LEBAR / 2
radius_vertikal = TINGGI / 2

# Posisi awal kumparan
y_awal = radius_horizontal * np.cos(sudut_oval)
z_awal = radius_vertikal * np.sin(sudut_oval)
x_awal = np.zeros_like(y_awal)

layar_x_awal, layar_y_awal = proyeksi_3d(
    x_awal, y_awal, z_awal
)

# Kawat utama kumparan
kumparan, = ax.plot(
    layar_x_awal,
    layar_y_awal,
    color=COPPER,
    linewidth=8,
    solid_capstyle="round",
    zorder=10
)

# Lapisan kilau kawat
kumparan_cahaya, = ax.plot(
    [], [],
    color="#FFD18A",
    linewidth=3,
    zorder=11
)

# Penanda material yang menempel pada kumparan
penanda_putaran, = ax.plot(
    [], [],
    linestyle="None",
    marker="o",
    markersize=8,
    markerfacecolor=YELLOW,
    markeredgecolor=WHITE,
    markeredgewidth=1.2,
    zorder=16
)

# Pusat poros
pusat = Circle(
    (0, 0),
    0.13,
    facecolor=ORANGE,
    edgecolor=WHITE,
    linewidth=1.5,
    zorder=17
)
ax.add_patch(pusat)

ax.add_patch(Circle(
    (0, 0),
    0.065,
    facecolor="#FFD18A",
    edgecolor=WHITE,
    linewidth=1,
    zorder=18
))

# ==========================================================
# KOMUTATOR
# ==========================================================

komutator_kiri = Rectangle(
    (-0.32, -2.05),
    0.22, 0.32,
    facecolor="#D78A42",
    edgecolor=WHITE,
    linewidth=1,
    zorder=8
)

komutator_kanan = Rectangle(
    (0.10, -2.05),
    0.22, 0.32,
    facecolor="#D78A42",
    edgecolor=WHITE,
    linewidth=1,
    zorder=8
)

ax.add_patch(komutator_kiri)
ax.add_patch(komutator_kanan)

ax.text(
    0, -2.25,
    "KOMUTATOR",
    ha="center", fontsize=7,
    color=YELLOW, weight="bold"
)

# ==========================================================
# PANAH ARUS DAN GAYA
# ==========================================================

panah_arus = FancyArrowPatch(
    (0, 0), (0, 0),
    arrowstyle="-|>",
    mutation_scale=20,
    color=ORANGE,
    linewidth=3,
    zorder=19
)
ax.add_patch(panah_arus)

panah_gaya_kiri = FancyArrowPatch(
    (0, 0), (0, 0),
    arrowstyle="-|>",
    mutation_scale=18,
    color=RED,
    linewidth=3,
    zorder=20
)

panah_gaya_kanan = FancyArrowPatch(
    (0, 0), (0, 0),
    arrowstyle="-|>",
    mutation_scale=18,
    color=YELLOW,
    linewidth=3,
    zorder=20
)

ax.add_patch(panah_gaya_kiri)
ax.add_patch(panah_gaya_kanan)

teks_arus = ax.text(
    0, -1.35,
    "ARAH ARUS LISTRIK",
    ha="center", fontsize=9,
    color=ORANGE, weight="bold"
)

ax.text(
    0, -1.75,
    "KUMPARAN KAWAT TEMBAGA OVAL",
    ha="center", fontsize=10,
    color=ORANGE, weight="bold"
)

teks_arah = ax.text(
    -4.5, 2.65,
    "ARAH ARUS: NORMAL",
    fontsize=9, color=YELLOW,
    weight="bold"
)

teks_sudut = ax.text(
    0, 2.55,
    "SUDUT GAYA: 90° | SUDUT TORSI: 90°",
    ha="center", fontsize=8,
    color=WHITE, weight="bold"
)

teks_komutator = ax.text(
    0, 2.25,
    "KOMUTATOR: NORMAL",
    ha="center", fontsize=8,
    color=GREEN, weight="bold"
)

ax.text(
    0, -2.65,
    "INTERAKSI ARUS LISTRIK DAN MEDAN MAGNET",
    ha="center", fontsize=8,
    color=GREY
)

# ==========================================================
# DASHBOARD
# ==========================================================

fig.text(
    0.735, 0.845,
    "MONITORING SISTEM",
    fontsize=13, color=WHITE,
    weight="bold"
)


def buat_panel(x, y, width, height, judul):

    panel = FancyBboxPatch(
        (x, y),
        width, height,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        transform=fig.transFigure,
        facecolor=PANEL,
        edgecolor=BLUE,
        linewidth=1.5,
        zorder=-1
    )

    fig.add_artist(panel)

    fig.text(
        x + 0.015,
        y + height - 0.035,
        judul,
        fontsize=10,
        color=CYAN,
        weight="bold"
    )


def buat_kartu(x, y, judul, warna):

    buat_panel(x, y, 0.215, 0.105, judul)

    return fig.text(
        x + 0.018,
        y + 0.025,
        "0.00",
        fontsize=19,
        color=warna,
        weight="bold"
    )


teks_B = buat_kartu(
    0.735, 0.705,
    "MEDAN MAGNET (B)", CYAN
)

teks_I = buat_kartu(
    0.735, 0.575,
    "ARUS LISTRIK (I)", ORANGE
)

teks_F = buat_kartu(
    0.735, 0.445,
    "GAYA LORENTZ (F)", YELLOW
)

teks_tau = buat_kartu(
    0.735, 0.315,
    "TORSI KUMPARAN", GREEN
)

buat_panel(
    0.735, 0.145,
    0.215, 0.135,
    "KETERANGAN FISIKA"
)

fig.text(
    0.755, 0.225,
    "F = B x I x L x sin(theta F)",
    fontsize=9, color=WHITE
)

fig.text(
    0.755, 0.195,
    "T = N x I x A x B x sin(theta T)",
    fontsize=8, color=CYAN
)

teks_status = fig.text(
    0.755, 0.105,
    "STATUS: MOTOR BERPUTAR",
    fontsize=9, color=GREEN,
    weight="bold"
)

teks_kecepatan = fig.text(
    0.755, 0.075,
    "KECEPATAN ANIMASI: 0.00 rad/s",
    fontsize=8, color=WHITE
)

teks_status_komutator = fig.text(
    0.755, 0.045,
    "KOMUTATOR: NORMAL",
    fontsize=8, color=ORANGE
)

# ==========================================================
# PERHITUNGAN FISIKA
# ==========================================================

def hitung_gaya():

    theta = np.radians(sudut_gaya)

    return (
        B * I * PANJANG *
        np.sin(theta)
    )


def hitung_torsi():

    theta = np.radians(sudut_torsi)

    return (
        JUMLAH_LILITAN *
        I *
        LUAS_LILITAN *
        B *
        np.sin(theta)
    )


# ==========================================================
# UPDATE DASHBOARD
# ==========================================================

def perbarui_panel():

    gaya = hitung_gaya()
    torsi = hitung_torsi()

    teks_B.set_text(f"{B:.2f} T")
    teks_I.set_text(f"{I:.2f} A")
    teks_F.set_text(f"{abs(gaya):.4f} N")
    teks_tau.set_text(f"{abs(torsi):.6f} N.m")

    teks_sudut.set_text(
        f"SUDUT GAYA: {sudut_gaya:.0f}° | "
        f"SUDUT TORSI: {sudut_torsi:.0f}°"
    )


# ==========================================================
# ANIMASI KUMPARAN
# POROS TETAP DIAM, KUMPARAN YANG BERPUTAR
# ==========================================================

def perbarui_visual(frame=None):

    global waktu

    torsi = abs(hitung_torsi())

    # Kecepatan visual mengikuti besar torsi
    kecepatan_visual = min(
        torsi * 200,
        3.0
    )

    if B <= 0 or I <= 0:
        kecepatan_visual = 0.0

    if berjalan and kecepatan_visual > 0:
        waktu += DT * kecepatan_visual * arah_arus

    fase = waktu

    # ------------------------------------------------------
    # ROTASI SELURUH KAWAT KUMPARAN PADA POROS HORIZONTAL
    # ------------------------------------------------------

    # Kumparan berbentuk oval pada bidang Y-Z.
    # Rotasi terjadi terhadap sumbu X.
    #
    # Poros lurus berada pada sumbu X dan tidak diubah.
    # Hanya koordinat Y dan Z kumparan yang berubah.

    y_putar = (
        y_awal * np.cos(fase)
        - z_awal * np.sin(fase)
    )

    z_putar = (
        y_awal * np.sin(fase)
        + z_awal * np.cos(fase)
    )

    x_putar = np.zeros_like(y_putar)

    layar_x, layar_y = proyeksi_3d(
        x_putar,
        y_putar,
        z_putar
    )

    # Mengubah posisi seluruh kawat oval
    kumparan.set_data(
        layar_x,
        layar_y
    )

    # ------------------------------------------------------
    # PENANDA MATERIAL MENEMPEL PADA KUMPARAN
    # ------------------------------------------------------

    sudut_penanda = fase * 0.8

    y_titik = (
        radius_horizontal * np.cos(sudut_penanda)
        * np.cos(fase)
        - radius_vertikal * np.sin(sudut_penanda)
        * np.sin(fase)
    )

    z_titik = (
        radius_horizontal * np.cos(sudut_penanda)
        * np.sin(fase)
        + radius_vertikal * np.sin(sudut_penanda)
        * np.cos(fase)
    )

    titik_x, titik_y = proyeksi_3d(
        0, y_titik, z_titik
    )

    penanda_putaran.set_data(
        [titik_x],
        [titik_y]
    )

    # ------------------------------------------------------
    # KILAU BERGERAK DI SEPANJANG KAWAT KUMPARAN
    # ------------------------------------------------------

    indeks = int(
        (fase * 25) % JUMLAH_TITIK_OVAL
    )

    indeks_cahaya = (
        np.arange(indeks, indeks + 18)
        % JUMLAH_TITIK_OVAL
    )

    kumparan_cahaya.set_data(
        layar_x[indeks_cahaya],
        layar_y[indeks_cahaya]
    )

    # ------------------------------------------------------
    # KOMUTATOR
    # ------------------------------------------------------

    setengah_putaran = int(
        np.floor(abs(fase) / np.pi)
    )

    arah_komutator = (
        1 if setengah_putaran % 2 == 0 else -1
    )

    arah_total = arah_arus * arah_komutator

    if arah_komutator == 1:

        teks_komutator.set_text(
            "KOMUTATOR: NORMAL"
        )

        teks_komutator.set_color(GREEN)

        teks_status_komutator.set_text(
            "KOMUTATOR: NORMAL"
        )

    else:

        teks_komutator.set_text(
            "KOMUTATOR: ARUS DIBALIK"
        )

        teks_komutator.set_color(YELLOW)

        teks_status_komutator.set_text(
            "KOMUTATOR: ARUS DIBALIK"
        )

    # ------------------------------------------------------
    # PANAH ARUS MENGIKUTI KAWAT KUMPARAN
    # ------------------------------------------------------

    indeks_arus = int(
        (abs(fase) / (2 * np.pi))
        * JUMLAH_TITIK_OVAL
    ) % JUMLAH_TITIK_OVAL

    indeks_sebelumnya = (
        indeks_arus - 5 * arah_total
    ) % JUMLAH_TITIK_OVAL

    indeks_sesudahnya = (
        indeks_arus + 5 * arah_total
    ) % JUMLAH_TITIK_OVAL

    awal = (
        layar_x[indeks_sebelumnya],
        layar_y[indeks_sebelumnya]
    )

    akhir = (
        layar_x[indeks_sesudahnya],
        layar_y[indeks_sesudahnya]
    )

    panah_arus.set_positions(
        awal,
        akhir
    )

    # ------------------------------------------------------
    # PANAH GAYA LORENTZ
    # ------------------------------------------------------

    gaya = abs(hitung_gaya())

    panjang_panah = min(
        gaya * 7.0,
        1.1
    )

    posisi_kiri = (-0.85, 0.0)
    posisi_kanan = (0.85, 0.0)

    if panjang_panah > 0.001:

        arah = arah_total

        panah_gaya_kiri.set_positions(
            posisi_kiri,
            (
                posisi_kiri[0],
                posisi_kiri[1] + panjang_panah * arah
            )
        )

        panah_gaya_kanan.set_positions(
            posisi_kanan,
            (
                posisi_kanan[0],
                posisi_kanan[1] - panjang_panah * arah
            )
        )

        panah_gaya_kiri.set_visible(True)
        panah_gaya_kanan.set_visible(True)

    else:

        panah_gaya_kiri.set_visible(False)
        panah_gaya_kanan.set_visible(False)

    # ------------------------------------------------------
    # INTENSITAS MEDAN MAGNET
    # ------------------------------------------------------

    intensitas = min(B / 2.0, 1.0)

    for simbol in simbol_magnet:

        simbol.set_alpha(
            0.15 + 0.85 * intensitas
        )

        simbol.set_markersize(
            5 + 7 * intensitas
        )

    for panah in panah_magnet:

        panah.set_alpha(
            0.15 + 0.85 * intensitas
        )

        panah.set_linewidth(
            0.8 + 1.8 * intensitas
        )

    # ------------------------------------------------------
    # ARAH ARUS MANUAL
    # ------------------------------------------------------

    if arah_arus == 1:

        teks_arah.set_text(
            "ARAH ARUS: NORMAL"
        )

        teks_arus.set_color(ORANGE)

    else:

        teks_arah.set_text(
            "ARAH ARUS: DIBALIK"
        )

        teks_arus.set_color(RED)

    # ------------------------------------------------------
    # STATUS MOTOR
    # ------------------------------------------------------

    if B <= 0 or I <= 0:

        teks_status.set_text(
            "STATUS: TIDAK ADA ARUS / MEDAN"
        )

        teks_status.set_color(RED)

    elif kecepatan_visual <= 0:

        teks_status.set_text(
            "STATUS: TORSI NOL"
        )

        teks_status.set_color(YELLOW)

    elif berjalan:

        teks_status.set_text(
            "STATUS: MOTOR BERPUTAR"
        )

        teks_status.set_color(GREEN)

    else:

        teks_status.set_text(
            "STATUS: MOTOR DIJEDA"
        )

        teks_status.set_color(RED)

    teks_kecepatan.set_text(
        f"KECEPATAN ANIMASI: {kecepatan_visual:.2f} rad/s"
    )

    perbarui_panel()

    return (
        kumparan,
        kumparan_cahaya,
        penanda_putaran,
        panah_arus,
        panah_gaya_kiri,
        panah_gaya_kanan
    )


# ==========================================================
# SLIDER PARAMETER
# ==========================================================

fig.text(
    0.055, 0.215,
    "ATUR PARAMETER SIMULASI",
    fontsize=10, color=CYAN,
    weight="bold"
)

ax_B = fig.add_axes(
    [0.19, 0.175, 0.32, 0.018],
    facecolor=PANEL
)

slider_B = Slider(
    ax_B, "Medan B (T)",
    0, 2, valinit=B_AWAL,
    color=BLUE
)

ax_I = fig.add_axes(
    [0.19, 0.135, 0.32, 0.018],
    facecolor=PANEL
)

slider_I = Slider(
    ax_I, "Arus I (A)",
    0, 10, valinit=I_AWAL,
    color=ORANGE
)

ax_sudut_gaya = fig.add_axes(
    [0.19, 0.095, 0.32, 0.018],
    facecolor=PANEL
)

slider_sudut_gaya = Slider(
    ax_sudut_gaya, "Sudut gaya",
    0, 180,
    valinit=SUDUT_GAYA_AWAL,
    valstep=1,
    color=GREEN
)

ax_sudut_torsi = fig.add_axes(
    [0.19, 0.055, 0.32, 0.018],
    facecolor=PANEL
)

slider_sudut_torsi = Slider(
    ax_sudut_torsi, "Sudut torsi",
    0, 180,
    valinit=SUDUT_TORSI_AWAL,
    valstep=1,
    color=YELLOW
)

for slider in (
    slider_B,
    slider_I,
    slider_sudut_gaya,
    slider_sudut_torsi
):

    slider.label.set_color(WHITE)
    slider.valtext.set_color(WHITE)
    slider.label.set_fontsize(8)


# ==========================================================
# CALLBACK SLIDER
# ==========================================================

def ubah_B(nilai):

    global B
    B = nilai

    perbarui_visual()
    fig.canvas.draw_idle()


def ubah_I(nilai):

    global I
    I = nilai

    perbarui_visual()
    fig.canvas.draw_idle()


def ubah_sudut_gaya(nilai):

    global sudut_gaya
    sudut_gaya = nilai

    perbarui_visual()
    fig.canvas.draw_idle()


def ubah_sudut_torsi(nilai):

    global sudut_torsi
    sudut_torsi = nilai

    perbarui_visual()
    fig.canvas.draw_idle()


slider_B.on_changed(ubah_B)
slider_I.on_changed(ubah_I)
slider_sudut_gaya.on_changed(ubah_sudut_gaya)
slider_sudut_torsi.on_changed(ubah_sudut_torsi)


# ==========================================================
# TOMBOL
# ==========================================================

ax_play = fig.add_axes(
    [0.56, 0.115, 0.14, 0.055]
)

tombol_play = Button(
    ax_play,
    "PLAY / PAUSE",
    color="#173D70",
    hovercolor="#2865A5"
)

tombol_play.label.set_color(WHITE)
tombol_play.label.set_fontweight("bold")

ax_reset = fig.add_axes(
    [0.73, 0.115, 0.11, 0.055]
)

tombol_reset = Button(
    ax_reset,
    "RESET",
    color="#087B58",
    hovercolor="#00A875"
)

tombol_reset.label.set_color(WHITE)
tombol_reset.label.set_fontweight("bold")

ax_reverse = fig.add_axes(
    [0.56, 0.045, 0.28, 0.055]
)

tombol_reverse = Button(
    ax_reverse,
    "BALIK ARAH ARUS",
    color="#742D91",
    hovercolor="#9B42BD"
)

tombol_reverse.label.set_color(WHITE)
tombol_reverse.label.set_fontweight("bold")


# ==========================================================
# PLAY / PAUSE
# ==========================================================

def play_pause(event):

    global berjalan

    berjalan = not berjalan

    if berjalan:
        animasi.event_source.start()
    else:
        animasi.event_source.stop()

    perbarui_visual()
    fig.canvas.draw_idle()


# ==========================================================
# RESET
# ==========================================================

def reset(event):

    global B, I
    global sudut_gaya, sudut_torsi
    global arah_arus, berjalan, waktu

    B = B_AWAL
    I = I_AWAL

    sudut_gaya = SUDUT_GAYA_AWAL
    sudut_torsi = SUDUT_TORSI_AWAL

    arah_arus = 1
    waktu = 0.0
    berjalan = True

    semua_slider = (
        slider_B,
        slider_I,
        slider_sudut_gaya,
        slider_sudut_torsi
    )

    for slider in semua_slider:
        slider.eventson = False

    slider_B.set_val(B_AWAL)
    slider_I.set_val(I_AWAL)
    slider_sudut_gaya.set_val(SUDUT_GAYA_AWAL)
    slider_sudut_torsi.set_val(SUDUT_TORSI_AWAL)

    for slider in semua_slider:
        slider.eventson = True

    animasi.event_source.start()

    perbarui_visual()
    fig.canvas.draw_idle()


# ==========================================================
# BALIK ARAH ARUS
# ==========================================================

def balik_arus(event):

    global arah_arus

    arah_arus *= -1

    perbarui_visual()
    fig.canvas.draw_idle()


tombol_play.on_clicked(play_pause)
tombol_reset.on_clicked(reset)
tombol_reverse.on_clicked(balik_arus)


# ==========================================================
# FOOTER
# ==========================================================

fig.text(
    0.035, 0.015,
    "MODERN SCIENCE DASHBOARD | HUKUM GAYA LORENTZ",
    fontsize=8, color=GREY
)

fig.text(
    0.78, 0.015,
    "PHYSICS ENGINEERING V12",
    fontsize=8, color=CYAN
)


# ==========================================================
# ANIMASI
# ==========================================================

perbarui_visual()

animasi = FuncAnimation(
    fig,
    perbarui_visual,
    interval=40,
    blit=False,
    cache_frame_data=False
)


# ==========================================================
# INFORMASI TERMINAL
# ==========================================================

print("=" * 60)
print("SIMULASI GAYA LORENTZ V12")
print("=" * 60)

print(f"Medan magnet       : {B:.2f} T")
print(f"Arus listrik       : {I:.2f} A")
print(f"Panjang kawat      : {PANJANG:.3f} m")
print(f"Sudut gaya         : {sudut_gaya} derajat")
print(f"Sudut torsi        : {sudut_torsi} derajat")
print(f"Jumlah lilitan     : {JUMLAH_LILITAN}")
print(f"Luas kumparan      : {LUAS_LILITAN:.6f} m2")

print("-" * 60)

print(f"Gaya Lorentz       : {hitung_gaya():.6f} N")
print(f"Torsi motor        : {hitung_torsi():.8f} N.m")

print("=" * 60)

plt.show()
