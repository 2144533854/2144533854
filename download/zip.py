import os
import zipfile

# path='/Users/storm.shen/web/qa/归档4/'
def check():
    return os.path.realpath(__file__).replace('zip.py','')
path=os.path.join(check(),'7mm_graph','jpg')
filelist=[]
filelist2=[]
max_size=10*1024*1024
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
def cal(s,list1,sum):

    for i in list1:
        file=os.path.join(s,i)

        sum+=os.path.getsize(file)
        print(file,sum)
    return sum
for i in range(len(filelist2)):

    if '/Users/storm.shen/web/izone/download/7mm_graph/jpg/.DS_Store' ==filelist2[i]:
        continue
    data=0
    list1 = os.listdir(filelist2[i])
    data=cal(filelist2[i],list1,data)

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
        if filenames=='/Users/storm.shen/web/izone/download/7mm_graph/jpg/.DS_Store':
            continue
        list2 = os.listdir(filenames)

        arcname = filenames[len(path):].strip(os.path.sep)  # 相对路径


        for i in list2:
            f1=os.path.join(filenames,i)
            f2=f'{arcname}-{i}'
            print(f1, f2)
            zipf.write(f1, f2)

    zipf.close()

def not_folder(numlist):
    j = 0
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

not_folder(numlist)
