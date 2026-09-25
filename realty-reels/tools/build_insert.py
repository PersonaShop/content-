"""Собирает вставку «пролёт» из клипа start->end:
hold на первом рендере (медленный наезд) -> клип с ускорением середины -> hold на последнем рендере.
Выход 1080x1920 (апскейл до финала — Topaz; тут только превью-сборка).

python build_insert.py clip.mp4 start.png end.png out.mp4 [--ramp 2.0]
"""
import argparse, subprocess, imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 1080, 1920, 30

def run(args):
    subprocess.run([FF, "-loglevel", "error", "-y", *args], check=True)

def still_push(img, out, dur, zoom_from, zoom_to):
    n = int(dur * FPS)
    z = f"{zoom_from}+({zoom_to}-{zoom_from})*on/{n}"
    run(["-loop", "1", "-i", img, "-vf",
         f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
         f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},format=yuv420p",
         "-frames:v", str(n), "-c:v", "libx264", "-crf", "16", out])

def ramp_clip(clip, out, ramp):
    # 0-35% 1x, 35-70% ускорение (пролёт), 70-100% 1x; + лёгкий motion blur через tmix в быстрой части
    probe = subprocess.run([FF, "-i", clip], capture_output=True, text=True).stderr
    dur = [l for l in probe.splitlines() if "Duration" in l][0].split("Duration: ")[1].split(",")[0]
    h, m, s = dur.split(":"); d = int(h)*3600 + int(m)*60 + float(s)
    a, b = d*0.35, d*0.70
    fc = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},split=3[v1][v2][v3];"
          f"[v1]trim=0:{a},setpts=PTS-STARTPTS[p1];"
          f"[v2]trim={a}:{b},setpts=(PTS-STARTPTS)/{ramp},tmix=frames=3[p2];"
          f"[v3]trim={b}:{d},setpts=PTS-STARTPTS[p3];"
          f"[p1][p2][p3]concat=n=3:v=1,fps={FPS}[v]")
    run(["-i", clip, "-filter_complex", fc, "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out])

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("clip"); ap.add_argument("start"); ap.add_argument("end"); ap.add_argument("out")
    ap.add_argument("--ramp", type=float, default=2.0)
    ap.add_argument("--hold", type=float, default=0.0, help="доп. наезд на стилле до/после клипа, с")
    a = ap.parse_args()
    ramp_clip(a.clip, "/tmp/_ramp.mp4", a.ramp)
    if a.hold > 0:
        # держим последний кадр самого клипа (а не стилл) — без скачка; медленный наезд
        run(["-sseof", "-0.05", "-i", "/tmp/_ramp.mp4", "-frames:v", "1", "/tmp/_last.png"])
        still_push("/tmp/_last.png", "/tmp/_end.mp4", a.hold, 1.0, 1.05)
        run(["-i", "/tmp/_ramp.mp4", "-i", "/tmp/_end.mp4", "-filter_complex",
             f"[0:v]fps={FPS},settb=1/{FPS},setpts=N/{FPS}/TB[a];[1:v]fps={FPS},settb=1/{FPS},setpts=N/{FPS}/TB[b];[a][b]concat=n=2:v=1[v]",
             "-map", "[v]", "-r", str(FPS), "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", a.out])
    else:
        run(["-i", "/tmp/_ramp.mp4", "-r", str(FPS), "-c:v", "libx264", "-crf", "16", a.out])
    print("ok", a.out)
