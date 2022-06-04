import os
import zipfile

# path='/Users/storm.shen/web/qa/归档4/'
def check():
    return os.path.realpath(__file__).replace('zip.py','')
path=os.path.join(check(),'7mm_graph','jpg')
filelist=[]
filelist2=[]
max_size=1024*1024*1024
filelist = os.listdir(path)
for i in filelist:
    filelist2.append(os.path.join(path,i))
# print(filelist2)
sum=0
num=0
numlist=[]
numlist.append(0)
if '/Users/storm.shen/web/qa/归档4/.DS_Store' in filelist2:
    filelist2.remove('/Users/storm.shen/web/qa/归档4/.DS_Store')
print(len(filelist2))
for i in range(len(filelist2)):
    data=os.path.getsize(filelist2[i])
    if sum<=max_size:
        sum+=data
    else:
        print(f"sum: {sum/1024/1024}   num  {i}")

        numlist.append(i)
        sum=0
        num=i
numlist.append(len(filelist2)-1)
print(numlist)
def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')

    for filenames in source_dir:
        # pathfile = os.path.join(path, filename)

        arcname = filenames[len(path):].strip(os.path.sep)  # 相对路径
        print(filenames,arcname)
        zipf.write(filenames, arcname)

    zipf.close()
j=0
for i in range(len(numlist)):
    name=f'{j}.zip'
    if i+1>=len(numlist):
        break
    elif numlist[i]!=0:
        make_zip(filelist2[numlist[i]+1:numlist[i+1]],name)
        print(numlist[i]+1,numlist[i+1])
    else:
        print(numlist[i], numlist[i + 1])
        make_zip(filelist2[numlist[i]:numlist[i + 1]], name)
    j+=1


