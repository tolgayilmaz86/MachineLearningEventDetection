import datetime

if __name__ == "__main__":
    csv_file = "C:\\Users\\tolga\\Downloads\\eventdetection\\nodejsCrawler\\tmp\\deprem.csv"
    arf_file = "C:\\Users\\tolga\\Downloads\\eventdetection\\nodejsCrawler\\tmp\\deprem.arff"

    formatted_data = ""
    with open(csv_file, 'r') as csvFile:
        csvreader = csvFile.readlines()
        for row in csvreader:
            data = row.split("|||")
            formatted_data += data[0] + "," + data[1] + "," + data[2] + ",\"" + datetime.datetime.fromtimestamp(int(data[3]))\
                .strftime('%Y-%m-%d %H:%M:%S') + "\"," + "\"" + \
                data[4].strip().replace("\"", " ").replace("\'", " ").replace(",", " ").strip() + "\"," + "DEPREM" + "\n"

    formatted_data = "@RELATION DEPREM\n\n" \
                     "@ATTRIBUTE screen_name string\n" \
                     "@ATTRIBUTE retweet_count numeric\n" \
                     "@ATTRIBUTE favorite_count numeric\n" \
                     "@ATTRIBUTE timestamp DATE \"yyyy-MM-dd HH:mm:ss\"\n" \
                     "@ATTRIBUTE tweet string \n" \
                     "@ATTRIBUTE event {TRAFIK,SEL,YANGIN,TEROR,DEPREM}\n" \
                     "@DATA\n"\
                     + formatted_data
    with open(arf_file, "w+") as result_file:
        result_file.write(formatted_data)
