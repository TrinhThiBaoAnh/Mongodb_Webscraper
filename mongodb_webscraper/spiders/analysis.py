import json
from collections import Counter
import datetime
import matplotlib.pyplot as plt
import pickle
import re
def clean_text(text):
    text = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}     /)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', text)
    text = re.sub(r'[^\w\s]','',text)
    text = text.replace(r'http(\S)+', r'')
    text = text.replace(r'http ...', r'')
    text = text.replace(r'(RT|rt)[ ]*@[ ]*[\S]+',r'')
    text = text.replace(r'@[\S]+',r'')
    text = text.replace(r'_[\S]?',r'')
    text = text.replace(r'[ ]{2, }',r' ')
    text = text.replace(r'&amp;?',r'and')
    text = text.replace(r'&lt;',r'<')
    text = text.replace(r'&gt;',r'>')
    text = text.replace(r'([\w\d]+)([^\w\d ]+)', r'\1 \2')
    text = text.replace(r'([^\w\d ]+)([\w\d]+)', r'\1 \2')
    text = text.lower()
    text = text.strip()
    return text

def text_preprocessing(string):
    string = string.strip().lower().replace('\ufeff','')
    string = re.sub(r"[(),.!?\'\`]", " ", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    string = re.sub(" +", " ", string)
    string = string.rstrip().lstrip()
    string = re.sub(r'([A-Z])\1+', lambda m: m.group(1).upper(), string, flags=re.IGNORECASE)
    return string
from collections import Counter
import itertools
def build_vocab(sentences):
    word_counts = Counter(itertools.chain(*sentences))
    vocabulary_inv = {x[0]:i+1 for i, x in enumerate(word_counts.most_common())}
#     vocabulary_inv['[CLS]'] = 1
    vocabulary_inv['pad'] = 0
#     vocabulary_inv['[SEP]'] = 2
    vocabulary = {i:x for i, x in vocabulary_inv.items()}
    return [vocabulary, vocabulary_inv]

# sent_train_pos = [s.split() for s in train_data['pos_tag']]
# vocab_pos, vocab_pos_inv = build_vocab(sent_train_pos)
def preprocess(text):
    print(type(text))
    text = text.lower().strip()
    text = clean_text(text)
    text = text_preprocessing(text)
    return txt
# counts word frequency using
# Counter from collections
def count_words_fast(text):	
	text = text.lower()
	skips = [".", ", ", ":", ";", "'", '"']
	for ch in skips:
		text = text.replace(ch, "")
	word_counts = Counter(text.split(" "))
	return word_counts
# word_counts = count_words_fast(text)
def word_stats(word_counts):	
	num_unique = len(word_counts)
	counts = word_counts.values()
	return (num_unique, counts)

def processing_author(author_lst):
    set_author = set(author_lst)
    print(set_author)
    with open('set_author.txt', 'w') as f:
        for item in set_author:
            f.write("%s\n" % item)

    stat_author = Counter(author_lst)
    my_dict = dict(stat_author)

    # Save dictionary to JSON file
    with open('stat_author.json', 'w', encoding='utf-8') as f:
        json.dump(my_dict, f)
    f.close()
    import numpy as np

    names = list(stat_author.keys())
    values = list(stat_author.values())
    
    for i in range(len(names)):
        if names[i] is None:
              names[i] = "unknown"
    print(names)
    plt.bar(names, values, width=0.2)
    plt.xlabel('Author Name')
    plt.ylabel('Num of articles')
    plt.title('Number of articles per author')
    plt.show()
def processing_date(date_lst):
    date_lst.sort(key=lambda x: x.date())
    groups = {}
    for date in date_lst:
        year = date.year
        if year not in groups:
            groups[year] = []
        groups[year].append(date)

    for year, dates in sorted(groups.items()):
        print(year, dates)
        count_by_month = Counter(date.month for date in dates)
        print(count_by_month)
    # ypoints = np.array([3, 8, 1, 10])

    # plt.plot(ypoints, color = 'r')
    # plt.show()
# def main():
    import pymongo
    from pymongo import MongoClient
    # Replace the following with your MongoDB Atlas connection string
    uri = "mongodb+srv://laptrinhmang:EKolZui6ZVocPcqR@cluster0.jxtulcr.mongodb.net/?retryWrites=true&w=majority"

    # Create a MongoClient to connect to MongoDB Atlas
    client = MongoClient(uri)

    # Access a database and collection
    db = client.reactionary
    viettan = db.viettan
    num_articles_vt = 0
    date_format2 = "%d/%m/%Y"
    author_lst2 = []
    date_lst2 = []
    items2 =[]
    #viettan statistics
    for item in viettan.find():
        # items.append(item)
        num_articles_vt = num_articles_vt + 1
        title = item["Title"][0]
        content = item["Content"]
        author = item["Author"]
        date= item["Date"]
        author_lst2.append(author)
        datetime_obj = datetime.datetime.strptime(date, date_format2)
        date_lst2.append(datetime_obj)
    # collection = db.articles
    # author_lst = []
    # date_lst = []
    # date_format = "%d/%m/%y, %H:%M"
    # # Find documents in the collection
    # items =[]

    # for item in collection.find():
    #     # items.append(item)
    #     title = item["title"][0]
    #     content = item["content"]
    #     author = item["author"]
    #     date= item["date"]
    #     author_lst.append(author)
    #     date_lst.append(date)
    #     datetime_obj = datetime.datetime.strptime(date, date_format)
    #     date_lst.append(datetime_obj)
    
    processing_author(author_lst2)
    # processing_date(date_lst)


if __name__ == "__main__":
    txt ="Ngày 19 tháng 1 năm nay đánh dấu 49 năm (1974-2023) ngày Trung Cộng ngang nhiên đánh chiếm quần đảo Hoàng Sa của Việt Nam, với sự hy sinh anh dũng của 74 sĩ quan và binh lính Hải quân Việt Nam Cộng Hòa.Trong những năm qua, những hành vi gây hấn của Trung Cộng tại Biển Đông ngày càng trắng trợn và mạnh bạo, gây nhiều thiệt hại nhân mạng và tài sản cho người dân Việt Nam. Từ việc đánh chiếm đảo Gạc Ma ở Trường Sa vào năm 1988 khiến 64 chiến sĩ Quân Đội Nhân Dân hy sinh, cho đến việc đưa ra Luật Hải Cảnh cho phép hải quân Trung Cộng bắn vào tàu và người Việt Nam trong vùng biển mà Trung Cộng đơn phương tuyên bố chủ quyền.Thế nhưng trong hơn bốn thập niên qua, nhà cầm quyền CSVN vẫn chưa làm đủ để minh định chủ quyền đối với Hoàng Sa, Trường Sa, giành lại lãnh thổ lãnh hải và bảo vệ người dân. Trong khi đó, người dân biểu tình chống Trung Cộng xâm lược, công khai lên án các hành vi gây hấn của Trung Cộng thì bị đàn áp, bỏ tù.Bắc Kinh đang mong muốn với thời gian kéo dài và sự phản đối yếu ớt của chính phủ CSVN thì Thế Giới sẽ quên rằng Trung Cộng đã chiếm Hoàng Sa bằng vũ lực.Vì vậy trong thời gian trước khi đến mốc điểm 50 năm Hoàng Sa bị cưỡng chiếm, Đảng Việt Tân kêu gọi những hành động cụ thể sau đây:Thứ nhất, hãy cùng nhau mạnh mẽ lên án hành vi xâm lược của Trung Cộng và đòi hỏi nhà nước CSVN thực hiện trách nhiệm bảo vệ chủ quyền, quyền lợi kinh tế và cuộc sống của ngư dân trên Biển Đông. Bắt đầu với việc trả tự do ngay lập tức cho những người Việt Nam yêu nước đang bị giam cầm vì chống Trung Cộng. Đồng thời không ngăn chặn các sinh hoạt quần chúng nhằm vinh danh sự hy sinh của các binh sĩ trong hai trận chiến Hoàng Sa và Trường Sa hay phản đối hành vi xâm lược của Trung Cộng.Thứ hai, đòi hỏi chính phủ CSVN phải quốc tế hóa việc Trung Cộng xâm phạm chủ quyền của Việt Nam và vô cớ tấn công ngư dân bằng cách mạnh mẽ lên án các hành vi bất hợp pháp của Bắc Kinh trước Liên Hiệp Quốc và kiện Trung Cộng ra tòa án Quốc tế.Thứ ba, Việt Nam cần kết hợp với các quốc gia tự do dân chủ trong khu vực để tạo sức mạnh liên minh nhằm ngăn cản sự bành trướng của Trung Cộng, bảo vệ hòa bình chung cũng như bảo vệ cuộc sống và sinh mệnh của ngư dân Việt Nam. Nếu Trung Cộng gây ra thiệt hại cho ngư dân, chính phủ CSVN phải đòi chính phủ Trung Quốc bồi thường thỏa đáng cho ngư dân.Việc Trung Cộng hiện đang bị các quốc gia tự do dân chủ xem là mối đe dọa cho an ninh và trật tự thế giới và với mốc điểm 50 năm sắp tới, đây là thời điểm quan trọng chúng ta cần đẩy mạnh các hoạt động để nhắc với Thế Giới rằng Hoàng Sa đã bị Trung Cộng cưỡng chiếm bằng vũ lực.Đảng Việt Tân mong cùng toàn dân Việt Nam đồng hành trong trách nhiệm chung: bảo vệ chủ quyền và người dân Việt Nam.Ngày 19 tháng 01 năm 2023Đảng Việt TânMọi chi tiết xin liên lạc: TS Đông Xuyến, +1 346-704-4744Liên quan đến vấn đề khai thác cát sông ở Đồng bằng Sông Cửu Long, hôm 17/3/2023, Văn phòng Chính phủ Việt Nam phát đi thông báo Số 79/TB-VPCP, yêu cầu “đơn giản hoá các thủ tục cấp phép mỏ vật liệu san lấp, nâng ngay công suất 50% ở các mỏ cát đang khai thác; cấp lại giấy phép khai thác các mỏ đã hết hạn, tạm thời đóng cửa; đưa vào hoạt động các mỏ mới phục vụ riêng cho các dự án cao tốc trên cơ sở quan trắc, giám sát chặt chẽ về môi trường, nguy cơ sạt lở theo đúng quy định của pháp luật.”Vợ chồng tôi đã nhiều lần nói rằng, chỉ có bọn xâm lược, đe dọa, lăm le xâm lược nước ta là thế lực thù địch. Còn tất cả người Việt Nam, dù ở trong hay ngoài nước, có quan điểm khác nhau, dù là đối lập, ở các đảng phái, hội đoàn khác nhau, yêu quê hương đất nước, đều là đồng bào mình, không phải thế lực thù địch. Chỉ ai có hành động bán nước, phá hoại đất nước, lúc đó pháp luật sẽ xử lý, lịch sử sẽ kết tội.Chính phủ Việt Nam hiện nay phải có những hành động cụ thể để khẳng định chủ quyền của Việt Nam đối với quần đảo Hoàng Sa và vùng biển lân cận, bao gồm: (i) lên án hành động chiếm đóng của Trung Quốc tại các cuộc họp của ASEAN và tại Đại Hội Đồng Liên Hiệp Quốc và (ii) đệ đơn kiện Bắc Kinh tại Tòa Án Trọng Tài Thường Trực ở The Hague.Đằng sau cuộc nói chuyện về hòa bình, bản chất của thượng đỉnh Tập-Putin sẽ đi theo hướng ngược lại, vì nó sẽ liên quan đến việc Trung Quốc gia tăng hỗ trợ cho Nga, trong lúc nước này tiến hành một cuộc chiến tranh xâm lược.Alexander Gabuev, một trong những nhà quan sát Trung Quốc hàng đầu tại Nga, hiện đang sống lưu vong, nhận xét rằng: “Đừng nhầm lẫn: chuyến đi sẽ nhằm thắt chặt quan hệ với Nga để mang về lợi ích cho Bắc Kinh, chứ không phải vì bất kỳ hoạt động trung gian hòa giải thực sự nào.”Việt Tân là một tập hợp những người Việt yêu dân chủvới khát vọng Canh Tân con người và Canh Tân Việt Namqua các hoạt động đấu tranh bất bạo động.© Copyright 2020 | Đảng Việt Tân"
    txt = preprocess(txt)
    print(txt)
    word_counts = count_words_fast(txt)
    print(word_counts.most_common(10))

