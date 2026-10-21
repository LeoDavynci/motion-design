import sys,glob
from PIL import Image,ImageDraw
fs=sorted(glob.glob('out/sheet/f*.png')); a=int(sys.argv[1]) if len(sys.argv)>1 else 0; b=int(sys.argv[2]) if len(sys.argv)>2 else len(fs)
fs=fs[a:b]; cols=4; w,h=480,270; rows=(len(fs)+cols-1)//cols
M=Image.new('RGB',(cols*w,rows*h))
for i,f in enumerate(fs):
    im=Image.open(f).convert('RGB').resize((w,h)); d=ImageDraw.Draw(im); d.text((6,4),f.split('_')[-1][:-4],fill=(255,255,0)); M.paste(im,((i%cols)*w,(i//cols)*h))
M.save('out/montage.png'); print(len(fs))
