from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import random
import io
import matplotlib.pyplot as plt
import kmeans

app = Flask(__name__)

points = []
centroids = []
init_method = "manual"
num_clusters = 0

@app.route('/submit_centroids', methods=['POST'])
def submit_centroids():
    global points
    global centroids
    global num_clusters

    data = request.get_json()
    print(data)
    user_centroids = data['centroids']
    if not num_clusters:
        num_clusters = int(data['num_clusters'])

    print(centroids)
    for centroid in user_centroids:
        print(centroid)
        x = centroid['x']
        y = centroid['y']
        if x is not None and y is not None and len(centroids) < num_clusters:
            centroids.append((x, y))
            plot_clusters(points, None, centroids, 'static/points.png')
        print(f'{num_clusters} and {len(centroids)}')

    return send_file('static/points.png', mimetype='image/png')


@app.route('/generate_dataset', methods=['POST'])
def generate_dataset():
    global points
    global num_clusters
    global centroids

    data = request.get_json()
    reset_data = True

    if data:
        print(data)
        reset_data = data['reset_data'] == 'true'
    
    if (reset_data):
        points = generate_random_points(100)
    else:                                     
        centroids = []
        num_clusters = int(data['num_clusters'])
        init_method = data['init_method']

        if init_method == 'random':
            centroids = random.sample(points, num_clusters)
        elif init_method == 'kmeans++':
            centroids = kmeans.kmeans_plus_plus_initialization(points,
                                                               num_clusters)
        elif init_method == 'farthest_first':
            centroids = kmeans.farthest_first_initialization(points, num_clusters)

    
    plot_clusters(points, None, centroids, 'static/points.png') 

    return send_file('static/points.png', mimetype='image/png')

@app.route('/step', methods=['POST'])
def step():
    global points
    global num_clusters
    global centroids

    if num_clusters != len(centroids):
        return send_file('static/points.png', mimetype='image/png')    
    
    clusters, centroids, converged = kmeans.kmeans(points, num_clusters,
                                                   centroids, 1)
    
    plot_clusters(points, clusters, centroids, 'static/plot.png')
        
    return send_file('static/plot.png', mimetype='image/png')


@app.route('/converge', methods=['POST'])
def converge():
    global points
    global num_clusters
    global centroids

    if num_clusters != len(centroids):
        return send_file('static/points.png', mimetype='image/png')
    
    clusters, centroids, converged = kmeans.kmeans(points,
                                                   num_clusters, centroids,
                                                   100)
    
    plot_clusters(points, clusters, centroids, 'static/plot.png')
        
    return send_file('static/plot.png', mimetype='image/png')

@app.route('/', methods=['GET', 'POST'])
def index():
    global points

    if not points:
        generate_dataset()      # for first req
        
    return render_template('index.html')

@app.route('/plot.png')
def show_plot():
    return send_file('static/plot.png', mimetype='image/png')

def generate_random_points(n):
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]

import matplotlib.pyplot as plt

def plot_clusters(points, clusters, centroids, plt_name):
    plt.figure(figsize=(8, 6))

    if clusters is None:
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        plt.scatter(x_coords, y_coords, c='gray', alpha=0.6)  # single color
        if centroids is not None:
            centroid_x = [c[0] for c in centroids]
            centroid_y = [c[1] for c in centroids]
            plt.scatter(centroid_x, centroid_y, c='black',
                        marker='x', s=100, label='Centroids')
    else:                       # cluster colors
        colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
        for idx, cluster in enumerate(clusters):
            x_coords = [p[0] for p in cluster]
            y_coords = [p[1] for p in cluster]
            plt.scatter(x_coords, y_coords, c=colors[idx % len(colors)],
                        label=f'Cluster {idx + 1}', alpha=0.6)

        centroid_x = [c[0] for c in centroids]
        centroid_y = [c[1] for c in centroids]
        plt.scatter(centroid_x, centroid_y, c='black', marker='x',
                    s=100, label='Centroids')

    # no margins so plot clickable
    plt.axis('tight')
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])
    plt.box(False)  # Hide the box outline
    
    # If centroids are present, show the legend
    if centroids is not None:
        plt.legend()
    
    # Save the figure without padding
    plt.savefig(plt_name, bbox_inches='tight', pad_inches=0)
    plt.close()

if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
