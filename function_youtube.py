
DEVELOPER_KEY = "AIzaSyDoyNLORaFsQfeNDoOwA78726OO3d6TS3o"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
def main():
    keyword_user=input("Enter the keyword")
    
    request = youtube.search().list(part="id,snippet",maxResults=10,q=keyword_user)
    video_links=[]

    '''
    For video_details
    '''
    title = []
    channelId = []
    channelTitle = []
    categoryId = []
    videoId = []
    viewCount = []
    likeCount = []
    dislikeCount = []
    commentCount = []
    favoriteCount = []
    category = []
    tags = []
    videos = []



    response = request.execute()
    print(response['items'])
    for item in response['items']:
        print("the video links are")
        if('videoId' in item['id']):
          video_links.append(item['id']['videoId'])  
          print(item['id']['videoId'])
          c=0

          '''
          for video_details
          '''
          title.append(item['snippet']['title'])
          videoId.append(item['id']['videoId'])
          #then collect stats on each video using videoId
          stats = youtube.videos().list(part='statistics, snippet',id=item['id']['videoId']).execute()
            
          channelId.append(stats['items'][0]['snippet']['channelId']) 
          channelTitle.append(stats['items'][0]['snippet']['channelTitle']) 
          categoryId.append(stats['items'][0]['snippet']['categoryId']) 
          favoriteCount.append(stats['items'][0]['statistics']['favoriteCount'])
          viewCount.append(stats['items'][0]['statistics']['viewCount'])
          #Not every video has likes/dislikes enabled so they won't appear in JSON response
          try:
              likeCount.append(stats['items'][0]['statistics']['likeCount'])
          except:
          #Good to be aware of Channels that turn off their Likes
              print("Video titled {0}, on Channel {1} Likes Count is not available".format(stats['items'][0]['snippet']['title'],stats['items'][0]['snippet']['channelTitle']))
              print(stats['items'][0]['statistics'].keys())
              #Appends "Not Available" to keep dictionary values aligned
              likeCount.append("Not available")
                
          try:
              dislikeCount.append(stats['items'][0]['statistics']['dislikeCount'])     
          except:
              #Good to be aware of Channels that turn off their Likes
              print("Video titled {0}, on Channel {1} Dislikes Count is not available".format(stats['items'][0]['snippet']['title'],stats['items'][0]['snippet']['channelTitle']))
              print(stats['items'][0]['statistics'].keys())
              dislikeCount.append("Not available")

          if 'commentCount' in stats['items'][0]['statistics'].keys():
              commentCount.append(stats['items'][0]['statistics']['commentCount'])
          else:
              commentCount.append(0)
         
          if 'tags' in stats['items'][0]['snippet'].keys():
              tags.append(stats['items'][0]['snippet']['tags'])
          else:
                #I'm not a fan of empty fields
              tags.append("No Tags")
                
    #Break out of for-loop and if statement and store lists of values in dictionary
    youtube_dict = {'tags':tags,'channelId': channelId,'channelTitle': channelTitle,'categoryId':categoryId,'title':title,'videoId':videoId,'viewCount':viewCount,'likeCount':likeCount,'dislikeCount':dislikeCount,'commentCount':commentCount,'favoriteCount':favoriteCount}
    print(youtube_dict)

    #Resume code
    video_rating_comment_based=[]
    for video in video_links:
        try:
          request = youtube.commentThreads().list(part="snippet,replies",videoId=video)
          comments_of_single_video = request.execute()
        except:
          video_rating_comment_based.append(-999999)
          continue

        print("The comments are")   
        comments_to_evaluate=[]
        for single_comment in comments_of_single_video['items']:
            a = normalize_corpus(single_comment['snippet']['topLevelComment']['snippet']['textDisplay'])
            print((a))
            comments_to_evaluate.append(a)

        print(score_reviews(comments_to_evaluate))
        video_rating_comment_based.append(score_reviews(comments_to_evaluate))

    url_rating_dict={}
    for url in video_links:
      for rating in video_rating_comment_based:
        url_rating_dict[url]=rating
        video_rating_comment_based.remove(rating) 
        break  
    return (url_rating_dict)

def remNonChar(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')
    
if __name__ == "__main__":
    main()
    