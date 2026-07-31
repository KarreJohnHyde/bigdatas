"""
Feature Analyzer - Load and analyze 224 user features
Includes: Education, Work, Location, Gender, Languages, etc.
"""

import os
import numpy as np
from pathlib import Path
from collections import defaultdict, Counter
import logging

logger = logging.getLogger(__name__)

class FeatureAnalyzer:
    """Analyze user features from Facebook dataset"""
    
    def __init__(self, data_dir='data/raw/facebook'):
        self.data_dir = Path(data_dir)
        self.ego_users = [0, 107, 1684, 1912, 3437, 348, 3980, 414, 686, 698]
        self.features = {}
        self.feature_names = {}
        self.user_features = {}
        
    def load_all_features(self):
        """Load all features from all ego networks"""
        logger.info("Loading features from all ego networks...")
        
        # Load feature names from first ego network
        self.feature_names = self._load_feature_names(0)
        
        # Load features from all ego networks
        for ego_id in self.ego_users:
            ego_features = self._load_ego_features(ego_id)
            self.user_features.update(ego_features)
            
        logger.info(f"Loaded features for {len(self.user_features)} users")
        return self.user_features
    
    def _load_feature_names(self, ego_id):
        """Load feature names from featnames file"""
        featnames_file = self.data_dir / f"{ego_id}.featnames"
        feature_names = {}
        
        try:
            with open(featnames_file, 'r') as f:
                for line in f:
                    parts = line.strip().split(' ', 1)
                    if len(parts) == 2:
                        idx = int(parts[0])
                        name = parts[1]
                        feature_names[idx] = name
            logger.info(f"Loaded {len(feature_names)} feature names")
        except Exception as e:
            logger.error(f"Error loading feature names: {e}")
            
        return feature_names
    
    def _load_ego_features(self, ego_id):
        """Load features for all users in an ego network"""
        feat_file = self.data_dir / f"{ego_id}.feat"
        egofeat_file = self.data_dir / f"{ego_id}.egofeat"
        features = {}
        
        # First, determine the number of features from the featnames file
        featnames_file = self.data_dir / f"{ego_id}.featnames"
        num_features = 0
        try:
            with open(featnames_file, 'r') as f:
                num_features = sum(1 for _ in f)
        except:
            num_features = 224  # Default
        
        try:
            # Load features for friends
            with open(feat_file, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) > 1:
                        user_id = int(parts[0])
                        feat_vector = [int(x) for x in parts[1:]]
                        # Pad or truncate to standard size
                        if len(feat_vector) < num_features:
                            feat_vector.extend([0] * (num_features - len(feat_vector)))
                        elif len(feat_vector) > num_features:
                            feat_vector = feat_vector[:num_features]
                        features[user_id] = np.array(feat_vector)
            
            # Load features for ego user
            with open(egofeat_file, 'r') as f:
                line = f.readline().strip()
                if line:
                    feat_vector = [int(x) for x in line.split()]
                    # Pad or truncate to standard size
                    if len(feat_vector) < num_features:
                        feat_vector.extend([0] * (num_features - len(feat_vector)))
                    elif len(feat_vector) > num_features:
                        feat_vector = feat_vector[:num_features]
                    features[ego_id] = np.array(feat_vector)
                    
            logger.info(f"Loaded features for {len(features)} users from ego network {ego_id} ({num_features} features)")
        except Exception as e:
            logger.error(f"Error loading features for ego {ego_id}: {e}")
            
        return features
    
    def get_user_profile(self, user_id):
        """Get comprehensive profile for a user"""
        if user_id not in self.user_features:
            return None
            
        features = self.user_features[user_id]
        
        profile = {
            'user_id': user_id,
            'birthday': self._extract_birthday(features),
            'education': self._extract_education(features),
            'gender': self._extract_gender(features),
            'hometown': self._extract_hometown(features),
            'location': self._extract_location(features),
            'languages': self._extract_languages(features),
            'work': self._extract_work(features),
            'feature_vector': features.tolist(),
            'total_features': int(np.sum(features))
        }
        
        return profile
    
    def _extract_birthday(self, features):
        """Extract birthday features (0-7)"""
        if len(features) < 8:
            return {'has_birthday': False}
        birthday_features = features[0:8]
        active_features = np.where(birthday_features == 1)[0]
        if len(active_features) > 0:
            return {
                'has_birthday': True,
                'features': active_features.tolist(),
                'count': len(active_features)
            }
        return {'has_birthday': False}
    
    def _extract_education(self, features):
        """Extract education features (8-72)"""
        feat_len = len(features)
        education = {
            'classes': self._get_active_features(features[8:min(13, feat_len)], 8) if feat_len > 8 else [],
            'concentration': self._get_active_features(features[13:min(20, feat_len)], 13) if feat_len > 13 else [],
            'degree': self._get_active_features(features[20:min(24, feat_len)], 20) if feat_len > 20 else [],
            'school': self._get_active_features(features[24:min(53, feat_len)], 24) if feat_len > 24 else [],
            'type': self._get_active_features(features[53:min(56, feat_len)], 53) if feat_len > 53 else [],
            'year': self._get_active_features(features[57:min(73, feat_len)], 57) if feat_len > 57 else []
        }
        
        # Calculate total education features
        total = sum(len(v) for v in education.values())
        education['total_education_features'] = total
        education['has_education'] = total > 0
        
        return education
    
    def _extract_gender(self, features):
        """Extract gender features (77-78)"""
        if len(features) < 79:
            return {'gender': 'Unknown'}
        gender_features = features[77:79]
        if len(gender_features) > 0 and gender_features[0] == 1:
            return {'gender': 'Male', 'feature': 77}
        elif len(gender_features) > 1 and gender_features[1] == 1:
            return {'gender': 'Female', 'feature': 78}
        return {'gender': 'Unknown'}
    
    def _extract_hometown(self, features):
        """Extract hometown features (79-89)"""
        feat_len = len(features)
        if feat_len < 79:
            return {'has_hometown': False, 'features': [], 'count': 0}
        hometown_features = features[79:min(90, feat_len)]
        active = self._get_active_features(hometown_features, 79)
        return {
            'has_hometown': len(active) > 0,
            'features': active,
            'count': len(active)
        }
    
    def _extract_location(self, features):
        """Extract current location features (128-139)"""
        feat_len = len(features)
        if feat_len < 128:
            return {'has_location': False, 'features': [], 'count': 0}
        location_features = features[128:min(140, feat_len)]
        active = self._get_active_features(location_features, 128)
        return {
            'has_location': len(active) > 0,
            'features': active,
            'count': len(active)
        }
    
    def _extract_languages(self, features):
        """Extract language features (90-103)"""
        feat_len = len(features)
        if feat_len < 90:
            return {'has_languages': False, 'features': [], 'count': 0, 'is_multilingual': False}
        language_features = features[90:min(104, feat_len)]
        active = self._get_active_features(language_features, 90)
        return {
            'has_languages': len(active) > 0,
            'features': active,
            'count': len(active),
            'is_multilingual': len(active) > 1
        }
    
    def _extract_work(self, features):
        """Extract work features (140-223)"""
        feat_len = len(features)
        work = {
            'employer': self._get_active_features(features[140:min(160, feat_len)], 140) if feat_len > 140 else [],
            'end_date': self._get_active_features(features[160:min(176, feat_len)], 160) if feat_len > 160 else [],
            'work_location': self._get_active_features(features[176:min(188, feat_len)], 176) if feat_len > 176 else [],
            'position': self._get_active_features(features[188:min(201, feat_len)], 188) if feat_len > 188 else [],
            'start_date': self._get_active_features(features[201:min(223, feat_len)], 201) if feat_len > 201 else [],
            'with': self._get_active_features(features[223:min(224, feat_len)], 223) if feat_len > 223 else []
        }
        
        total = sum(len(v) for v in work.values())
        work['total_work_features'] = total
        work['has_work'] = total > 0
        
        return work
    
    def _get_active_features(self, feature_subset, offset=0):
        """Get list of active feature indices"""
        active = np.where(feature_subset == 1)[0]
        return [int(i + offset) for i in active]
    
    def calculate_similarity(self, user1_id, user2_id):
        """Calculate similarity between two users (Jaccard similarity)"""
        if user1_id not in self.user_features or user2_id not in self.user_features:
            return 0.0
            
        features1 = self.user_features[user1_id]
        features2 = self.user_features[user2_id]
        
        # Handle different feature lengths by padding to same size
        max_len = max(len(features1), len(features2))
        if len(features1) < max_len:
            features1 = np.pad(features1, (0, max_len - len(features1)), 'constant')
        if len(features2) < max_len:
            features2 = np.pad(features2, (0, max_len - len(features2)), 'constant')
        
        # Jaccard similarity: intersection / union
        intersection = np.sum(np.logical_and(features1, features2))
        union = np.sum(np.logical_or(features1, features2))
        
        if union == 0:
            return 0.0
        
        return float(intersection / union)
    
    def find_similar_users(self, user_id, top_n=10):
        """Find most similar users to a given user"""
        if user_id not in self.user_features:
            return []
            
        similarities = []
        for other_id in self.user_features:
            if other_id != user_id:
                sim = self.calculate_similarity(user_id, other_id)
                similarities.append((other_id, sim))
        
        # Sort by similarity descending
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_n]
    
    def analyze_homophily(self, G):
        """Analyze if similar users connect more (homophily)"""
        logger.info("Analyzing homophily...")
        
        # Sample edges to avoid too long computation
        edges = list(G.edges())
        sample_size = min(1000, len(edges))
        sampled_edges = np.random.choice(len(edges), sample_size, replace=False)
        
        connected_similarities = []
        not_connected_similarities = []
        
        # Calculate similarity for connected users
        for idx in sampled_edges:
            u, v = edges[idx]
            if u in self.user_features and v in self.user_features:
                sim = self.calculate_similarity(u, v)
                connected_similarities.append(sim)
        
        # Calculate similarity for random non-connected pairs
        nodes = list(G.nodes())
        for _ in range(sample_size):
            u = np.random.choice(nodes)
            v = np.random.choice(nodes)
            if u != v and not G.has_edge(u, v):
                if u in self.user_features and v in self.user_features:
                    sim = self.calculate_similarity(u, v)
                    not_connected_similarities.append(sim)
        
        connected_avg = np.mean(connected_similarities) if connected_similarities else 0
        not_connected_avg = np.mean(not_connected_similarities) if not_connected_similarities else 0
        
        homophily_score = connected_avg - not_connected_avg
        
        return {
            'connected_similarity_avg': float(connected_avg),
            'not_connected_similarity_avg': float(not_connected_avg),
            'homophily_score': float(homophily_score),
            'homophily_exists': bool(homophily_score > 0),
            'interpretation': 'Strong homophily' if homophily_score > 0.1 else 
                            'Moderate homophily' if homophily_score > 0.05 else 
                            'Weak homophily' if homophily_score > 0 else 'No homophily'
        }
    
    def analyze_education_communities(self):
        """Find communities based on education (schools)"""
        logger.info("Analyzing education-based communities...")
        
        school_communities = defaultdict(list)
        
        for user_id, features in self.user_features.items():
            # Get school features (24-52)
            schools = self._get_active_features(features[24:53], 24)
            for school in schools:
                school_communities[school].append(user_id)
        
        # Filter communities with at least 2 members
        communities = {k: v for k, v in school_communities.items() if len(v) >= 2}
        
        return {
            'total_schools': len(communities),
            'largest_school_size': max([len(v) for v in communities.values()]) if communities else 0,
            'avg_school_size': np.mean([len(v) for v in communities.values()]) if communities else 0,
            'communities': {f'School_{k}': v for k, v in list(communities.items())[:20]}
        }
    
    def analyze_work_networks(self):
        """Find networks based on work (employers)"""
        logger.info("Analyzing work-based networks...")
        
        work_networks = defaultdict(list)
        
        for user_id, features in self.user_features.items():
            # Get employer features (140-159)
            employers = self._get_active_features(features[140:160], 140)
            for employer in employers:
                work_networks[employer].append(user_id)
        
        # Filter networks with at least 2 members
        networks = {k: v for k, v in work_networks.items() if len(v) >= 2}
        
        return {
            'total_companies': len(networks),
            'largest_company_size': max([len(v) for v in networks.values()]) if networks else 0,
            'avg_company_size': np.mean([len(v) for v in networks.values()]) if networks else 0,
            'networks': {f'Company_{k}': v for k, v in list(networks.items())[:20]}
        }
    
    def analyze_location_clusters(self):
        """Find clusters based on location"""
        logger.info("Analyzing location-based clusters...")
        
        location_clusters = defaultdict(list)
        
        for user_id, features in self.user_features.items():
            # Get location features (128-139)
            locations = self._get_active_features(features[128:140], 128)
            for location in locations:
                location_clusters[location].append(user_id)
        
        # Filter clusters with at least 2 members
        clusters = {k: v for k, v in location_clusters.items() if len(v) >= 2}
        
        return {
            'total_locations': len(clusters),
            'largest_location_size': max([len(v) for v in clusters.values()]) if clusters else 0,
            'avg_location_size': np.mean([len(v) for v in clusters.values()]) if clusters else 0,
            'clusters': {f'Location_{k}': v for k, v in list(clusters.items())[:20]}
        }
    
    def analyze_gender_patterns(self):
        """Analyze gender distribution and patterns"""
        logger.info("Analyzing gender patterns...")
        
        gender_counts = {'Male': 0, 'Female': 0, 'Unknown': 0}
        
        for user_id, features in self.user_features.items():
            gender = self._extract_gender(features)
            gender_counts[gender['gender']] += 1
        
        total = sum(gender_counts.values())
        
        return {
            'male_count': gender_counts['Male'],
            'female_count': gender_counts['Female'],
            'unknown_count': gender_counts['Unknown'],
            'male_percentage': (gender_counts['Male'] / total * 100) if total > 0 else 0,
            'female_percentage': (gender_counts['Female'] / total * 100) if total > 0 else 0,
            'gender_ratio': (gender_counts['Male'] / gender_counts['Female']) if gender_counts['Female'] > 0 else 0
        }
    
    def get_comprehensive_analysis(self, G):
        """Get all advanced analyses"""
        logger.info("Running comprehensive feature analysis...")
        
        analysis = {
            'homophily': self.analyze_homophily(G),
            'education_communities': self.analyze_education_communities(),
            'work_networks': self.analyze_work_networks(),
            'location_clusters': self.analyze_location_clusters(),
            'gender_patterns': self.analyze_gender_patterns(),
            'total_users_with_features': len(self.user_features)
        }
        
        logger.info("Comprehensive analysis complete")
        return analysis

