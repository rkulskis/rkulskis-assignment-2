import random
import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) # euclidian


def random_initialization(points, k):
    return random.sample(points, k)

def farthest_first_initialization(points, k):
    centroids = [random.choice(points)]  # start with rand
    while len(centroids) < k:
        # dist from pts to closest centroid
        distances = [min(distance(point, centroid)
                         for centroid in centroids) for point in points]
        # select pt with the maximum distance to any centroid
        farthest_point = points[distances.index(max(distances))]
        centroids.append(farthest_point)
    return centroids

def kmeans_plus_plus_initialization(points, k):
    centroids = [random.choice(points)]  # start w/ one rand centroid
    while len(centroids) < k:
        distances = [min(distance(point, centroid) for centroid in centroids) for point in points]
        # next centroid based on weighted probability
        total_distance = sum(distances)
        probabilities = [d / total_distance for d in distances]
        new_centroid = random.choices(points, weights=probabilities)[0]
        centroids.append(new_centroid)
    return centroids

def assign_clusters(points, centroids):
    clusters = [[] for _ in centroids]
    for point in points:
        distances = [distance(point, centroid) for centroid in centroids]
        nearest = distances.index(min(distances))
        clusters[nearest].append(point)
    return clusters

def calculate_new_centroids(clusters):
    centroids = []
    for cluster in clusters:
        if cluster:  # avoid division by 0
            x_coords = [point[0] for point in cluster]
            y_coords = [point[1] for point in cluster]
            centroid = (sum(x_coords) / len(cluster), sum(y_coords) / len(cluster))
        centroids.append(centroid)
    return centroids

def kmeans(points, k, centroids, iter):
    converged = False
    for _ in range(iter):
        clusters = assign_clusters(points, centroids)
        new_centroids = calculate_new_centroids(clusters)
        if centroids == new_centroids:
            converged = True
            print("converged!")
            break
        centroids = new_centroids
    return clusters, centroids, converged
