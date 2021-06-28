dogs = [
    {
        "name" : "Melba",
        "handle" : "melba",
        "bio" : "Hi, I'm Melba! I'm a mini-goldendoodle and I love to play.",
        "age" : 3
    },
    {
        "name" : "Charlie",
        "handle" : "chucky",
        "bio" : "Hi I'm Charlie! I'm a big white standard poodle.",
        "age" : 7
    },
    {
        "name" : "Rosie",
        "handle" : "rose",
        "bio" : "Hi I'm Rosie! I'm from the hard streets of LA, don't mess with me.",
        "age" : 9
    }
]


timerData = [
    {
        "name" : "Test1",
        "currentTimeH" : 0,
        "currentTimeM" : 0,
        "totalTime" : 0
    },
    {
        "name" : "Test2",
        "currentTimeH" : 2,
        "currentTimeM" : 9,
        "totalTime" : 0,
    },
    {
        "name" : "Test3",
        "currentTimeH" : 0,
        "currentTimeM" : 20,
        "totalTime" : 400,
    },
  
]

def get_dog_by_handle(handle):
    for dog in dogs:
        if dog['handle'] == handle:
            return dog
    return None

days = [
    {
        "day" : "Monday",
        "id" : 1
    },
    {
        "day" : "Tuesday",
        "id" : 2
    },
    {
        "day" : "Wednesday",
        "id" : 3
    },
    
    {
        "day" : "Thursday",
        "id" : 4
    },
    {
        "day" : "Friday",
        "id" : 5
    },
    {
        "day" : "Saturday",
        "id" : 6
    },
    {
        "day" : "Sunday",
        "id" : 7
    }
   
]

def add_post_url():
    results = []
    for post in posts:
        for dog in dogs:
            sub = "@" + dog['handle']
            print(sub)
            if sub in post['text']:
                link = '<a href="/dog/' +dog['handle'] + '">' + sub + '</a>'
                post['text'] = post['text'].replace(sub, link)     
        results.append(post)
    return results

def get_posts_by_handle(handle):
    results = []
    url_posts = add_post_url()
    for post in url_posts:
        if post['handle'] == handle:
            results.append(post)
    return results

def get_post_by_id(id):
    for post in posts:
        if post['id'] == id:
            return post
    return None