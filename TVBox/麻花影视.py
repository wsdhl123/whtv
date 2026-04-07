from flask import Flask, render_template, request, jsonify
from spider import Spider

app = Flask(__name__)

# 初始化爬虫
spider = Spider()
spider.init({})

# 缓存数据
movies_cache = {}
categories = spider.homeContent({})['class']

@app.route('/')
def index():
    # 获取分类参数
    cid = request.args.get('cid', '1')  # 默认电影分类
    page = request.args.get('page', '1')
    
    # 从缓存获取数据或从爬虫获取
    cache_key = f'{cid}_{page}'
    if cache_key not in movies_cache:
        movies_data = spider.categoryContent(cid, page, {}, {})['list']
        movies_cache[cache_key] = movies_data
    else:
        movies_data = movies_cache[cache_key]
    
    # 转换数据格式以适应模板
    movies = []
    for item in movies_data:
        movies.append({
            'id': item['vod_id'],
            'title': item['vod_name'],
            'genre': item.get('vod_remarks', ''),
            'year': '',
            'rating': 0,
            'description': '',
            'poster': item['vod_pic'],
            'url': f'/movie/{item["vod_id"]}'
        })
    
    return render_template('index.html', movies=movies, genres=categories, years=[], cid=cid, page=page)

@app.route('/movie/<movie_id>')
def movie_detail(movie_id):
    # 从爬虫获取电影详情
    movie_data = spider.detailContent([movie_id])['list']
    if not movie_data:
        return "电影不存在", 404
    movie_data = movie_data[0]
    
    # 转换数据格式以适应模板
    movie = {
        'id': movie_data['vod_id'],
        'title': movie_data['vod_name'],
        'genre': movie_data.get('type_name', ''),
        'year': movie_data.get('vod_year', ''),
        'rating': 0,
        'description': movie_data.get('vod_content', ''),
        'poster': f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={movie_data['vod_name']}%20movie%20poster&image_size=square_hd",
        'url': '#'
    }
    
    # 处理播放地址
    if 'vod_play_url' in movie_data:
        play_urls = movie_data['vod_play_url'].split('#')
        if play_urls:
            first_play = play_urls[0].split('$')
            if len(first_play) == 2:
                play_url = spider.get_play_data(first_play[1])
                movie['url'] = play_url
    
    return render_template('movie_detail.html', movie=movie)

@app.route('/api/movies')
def api_movies():
    # 获取首页电影数据
    movies_data = spider.homeVideoContent()['list']
    # 转换数据格式
    movies = []
    for item in movies_data:
        movies.append({
            'id': item['vod_id'],
            'title': item['vod_name'],
            'genre': item.get('vod_remarks', ''),
            'poster': item['vod_pic']
        })
    return jsonify(movies)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
