from PIL import Image
import numpy as np, json
S='fig1x/'
def fix(im):
    A=np.asarray(im.convert('RGB')).copy(); h,w=A.shape[:2]
    for y in list(range(0,40))+list(range(h-40,h)):
        d=min(y,h-1-y); ins=int(round(40-np.sqrt(max(0,40*40-(40-d)**2))))+6; src=min(ins+8,w//2)
        A[y,:ins]=A[y,src]; A[y,w-ins:]=A[y,w-1-src]
    A[:3]=A[3:4]; A[h-3:]=A[h-4:h-3]
    A[:,:3]=A[:,3:4]; A[:,w-3:]=A[:,w-4:w-3]
    return Image.fromarray(A)
up=lambda im:(lambda f:f.resize((f.width*2,f.height*2),Image.LANCZOS))(fix(im))
names={'profile_top':'profile_177_21620','processing':'processing_294_22950','skeleton':'skeleton_294_23017','preview':'preview_294_23081','home_map':'home_183_4842',
 'ask_1_suggest':'ask_suggest_294_31691','ask_2_query':'ask_query_294_31833','ask_3_thinking':'ask_thinking_294_32257','ask_4_results':'ask_results_294_32745','ask_4b_results_draft':'ask_results2_294_32790','ask_5_copied':'ask_copied_294_32870','profile_scrolled':'profile_scrolled_177_25472'}
for o,i in names.items(): up(Image.open(S+i+'.png')).save(o+'.png')
a=Image.open(S+'profile_177_21620.png').convert('RGB'); b=Image.open(S+'profile_scrolled_177_25472.png').convert('RGB'); c=Image.open(S+'moment_294_31110.png').convert('RGB')
SEAM=750; OFF=601; H=OFF+844
page=Image.new('RGB',(390,H)); page.paste(a.crop((0,0,390,SEAM)),(0,0))
page.paste(c.crop((0,SEAM-OFF,390,844)),(0,SEAM))
# blend 10px across the seam
A=np.asarray(a,dtype=float);C=np.asarray(c,dtype=float);P=np.asarray(page,dtype=float)
for k in range(10):
    w=k/10; y=SEAM-10+k; P[y]=A[y]*(1-w)+C[y-OFF]*w
page=Image.fromarray(P.astype('uint8'))
page=page.crop((0,0,390,H-30)); up(page).save('profile_full.png')
up(b.crop((0,0,390,130))).save('profile_header_compact.png')
up(c.crop((0,745,390,844))).save('profile_composer.png')
print(page.size)
