import time, sys; sys.path.insert(0, ".")
from chapter_engine import run
t0=time.time()
ch=run(srt_path=r"E:\新版YouTube下载视频\movie_full_subtitles.srt",gap=20)
print(f"{time.time()-t0:.1f}s {len(ch)}章")
for c in ch[:8]: 
    v = "[V]" if c["verified"] else "[ ]"
    print(f"  {v} {c['timestamp']} {c['title'][:25]}")
