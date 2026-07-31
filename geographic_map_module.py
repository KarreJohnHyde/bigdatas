"""
Fresh Geographic Map Module for Facebook Social Network Analysis
This module handles all geographic visualization functionality separately
"""

import random
import time
from flask import Blueprint, render_template, jsonify

# Create blueprint for geographic map
geographic_bp = Blueprint('geographic', __name__, url_prefix='/geographic')

# Global cities with realistic distribution across ALL continents
MAJOR_CITIES = [
    # North America - Dense coverage
    {'lat': 40.7128, 'lon': -74.0060, 'name': 'New York', 'weight': 25, 'continent': 'North America'},
    {'lat': 34.0522, 'lon': -118.2437, 'name': 'Los Angeles', 'weight': 22},
    {'lat': 41.8781, 'lon': -87.6298, 'name': 'Chicago', 'weight': 18},
    {'lat': 29.7604, 'lon': -95.3698, 'name': 'Houston', 'weight': 15},
    {'lat': 33.4484, 'lon': -112.0740, 'name': 'Phoenix', 'weight': 12},
    {'lat': 25.7617, 'lon': -80.1918, 'name': 'Miami', 'weight': 12},
    {'lat': 39.7392, 'lon': -104.9903, 'name': 'Denver', 'weight': 10},
    {'lat': 47.6062, 'lon': -122.3321, 'name': 'Seattle', 'weight': 10},
    {'lat': 43.6532, 'lon': -79.3832, 'name': 'Toronto', 'weight': 15},
    {'lat': 45.5017, 'lon': -73.5673, 'name': 'Montreal', 'weight': 12},
    {'lat': 49.2827, 'lon': -123.1207, 'name': 'Vancouver', 'weight': 8},
    {'lat': 32.7767, 'lon': -96.7970, 'name': 'Dallas', 'weight': 10},
    {'lat': 40.7589, 'lon': -111.8882, 'name': 'Salt Lake City', 'weight': 6},
    {'lat': 44.9778, 'lon': -93.2650, 'name': 'Minneapolis', 'weight': 8},
    {'lat': 39.9526, 'lon': -75.1652, 'name': 'Philadelphia', 'weight': 10},
    {'lat': 42.3601, 'lon': -71.0589, 'name': 'Boston', 'weight': 9},
    {'lat': 33.7490, 'lon': -84.3880, 'name': 'Atlanta', 'weight': 8},
    {'lat': 41.8781, 'lon': -87.6298, 'name': 'Detroit', 'weight': 6},
    {'lat': 25.7617, 'lon': -80.1918, 'name': 'Orlando', 'weight': 5},
    {'lat': 36.1699, 'lon': -115.1398, 'name': 'Las Vegas', 'weight': 5},
    
    # Europe - Comprehensive coverage
    {'lat': 51.5074, 'lon': -0.1278, 'name': 'London', 'weight': 22, 'continent': 'Europe'},
    {'lat': 48.8566, 'lon': 2.3522, 'name': 'Paris', 'weight': 20},
    {'lat': 52.5200, 'lon': 13.4050, 'name': 'Berlin', 'weight': 18},
    {'lat': 41.9028, 'lon': 12.4964, 'name': 'Rome', 'weight': 15},
    {'lat': 40.4168, 'lon': -3.7038, 'name': 'Madrid', 'weight': 15},
    {'lat': 52.3676, 'lon': 4.9041, 'name': 'Amsterdam', 'weight': 12},
    {'lat': 55.7558, 'lon': 37.6176, 'name': 'Moscow', 'weight': 15},
    {'lat': 59.9311, 'lon': 10.7579, 'name': 'Oslo', 'weight': 8},
    {'lat': 55.6761, 'lon': 12.5683, 'name': 'Copenhagen', 'weight': 10},
    {'lat': 50.0755, 'lon': 14.4378, 'name': 'Prague', 'weight': 10},
    {'lat': 48.2082, 'lon': 16.3738, 'name': 'Vienna', 'weight': 10},
    {'lat': 46.9481, 'lon': 7.4474, 'name': 'Zurich', 'weight': 8},
    {'lat': 59.4370, 'lon': 24.7536, 'name': 'Tallinn', 'weight': 5},
    {'lat': 50.8503, 'lon': 4.3517, 'name': 'Brussels', 'weight': 8},
    {'lat': 60.1699, 'lon': 24.9384, 'name': 'Helsinki', 'weight': 8},
    {'lat': 55.9533, 'lon': -3.1883, 'name': 'Edinburgh', 'weight': 6},
    {'lat': 53.3498, 'lon': -6.2603, 'name': 'Dublin', 'weight': 6},
    {'lat': 41.3851, 'lon': 2.1734, 'name': 'Barcelona', 'weight': 10},
    {'lat': 45.4642, 'lon': 9.1900, 'name': 'Milan', 'weight': 10},
    {'lat': 52.2297, 'lon': 21.0122, 'name': 'Warsaw', 'weight': 8},
    
    # Asia - Extensive coverage
    {'lat': 35.6762, 'lon': 139.6503, 'name': 'Tokyo', 'weight': 25, 'continent': 'Asia'},
    {'lat': 22.3193, 'lon': 114.1694, 'name': 'Hong Kong', 'weight': 15},
    {'lat': 1.3521, 'lon': 103.8198, 'name': 'Singapore', 'weight': 12},
    {'lat': 37.5665, 'lon': 126.9780, 'name': 'Seoul', 'weight': 18},
    {'lat': 39.9042, 'lon': 116.4074, 'name': 'Beijing', 'weight': 20},
    {'lat': 31.2304, 'lon': 121.4737, 'name': 'Shanghai', 'weight': 20},
    {'lat': 19.0760, 'lon': 72.8777, 'name': 'Mumbai', 'weight': 15},
    {'lat': 28.7041, 'lon': 77.1025, 'name': 'Delhi', 'weight': 15},
    {'lat': 13.7563, 'lon': 100.5018, 'name': 'Bangkok', 'weight': 12},
    {'lat': 14.5995, 'lon': 120.9842, 'name': 'Manila', 'weight': 10},
    {'lat': 12.9716, 'lon': 77.5946, 'name': 'Bangalore', 'weight': 10},
    {'lat': 17.3850, 'lon': 78.4867, 'name': 'Hyderabad', 'weight': 8},
    {'lat': 22.5726, 'lon': 88.3639, 'name': 'Kolkata', 'weight': 10},
    {'lat': 18.5204, 'lon': 73.8567, 'name': 'Pune', 'weight': 8},
    {'lat': 25.2048, 'lon': 55.2708, 'name': 'Dubai', 'weight': 10},
    {'lat': 24.7136, 'lon': 46.6753, 'name': 'Riyadh', 'weight': 8},
    {'lat': 31.7683, 'lon': 35.2137, 'name': 'Jerusalem', 'weight': 5},
    {'lat': 33.3152, 'lon': 44.3661, 'name': 'Baghdad', 'weight': 5},
    {'lat': 35.6892, 'lon': 51.3890, 'name': 'Tehran', 'weight': 8},
    {'lat': 24.8607, 'lon': 67.0011, 'name': 'Karachi', 'weight': 10},
    {'lat': 33.6844, 'lon': 73.0479, 'name': 'Islamabad', 'weight': 5},
    {'lat': 23.8103, 'lon': 90.4125, 'name': 'Dhaka', 'weight': 8},
    {'lat': 6.2088, 'lon': 106.8456, 'name': 'Jakarta', 'weight': 10},
    {'lat': 3.1390, 'lon': 101.6869, 'name': 'Kuala Lumpur', 'weight': 8},
    {'lat': 25.0330, 'lon': 121.5654, 'name': 'Taipei', 'weight': 8},
    
    # Australia & Oceania
    {'lat': -33.8688, 'lon': 151.2093, 'name': 'Sydney', 'weight': 12, 'continent': 'Australia'},
    {'lat': -37.8136, 'lon': 144.9631, 'name': 'Melbourne', 'weight': 10},
    {'lat': -36.8485, 'lon': 174.7633, 'name': 'Auckland', 'weight': 6},
    {'lat': -31.9505, 'lon': 115.8605, 'name': 'Perth', 'weight': 8},
    {'lat': -27.4698, 'lon': 153.0251, 'name': 'Brisbane', 'weight': 8},
    {'lat': -34.9285, 'lon': 138.6007, 'name': 'Adelaide', 'weight': 5},
    
    # South America - Good coverage
    {'lat': -23.5505, 'lon': -46.6333, 'name': 'São Paulo', 'weight': 15, 'continent': 'South America'},
    {'lat': -22.9068, 'lon': -43.1729, 'name': 'Rio de Janeiro', 'weight': 12},
    {'lat': -34.6118, 'lon': -58.3960, 'name': 'Buenos Aires', 'weight': 12},
    {'lat': -12.0464, 'lon': -77.0428, 'name': 'Lima', 'weight': 8},
    {'lat': 4.7110, 'lon': -74.0721, 'name': 'Bogotá', 'weight': 8},
    {'lat': -33.4489, 'lon': -70.6693, 'name': 'Santiago', 'weight': 8},
    {'lat': -15.7801, 'lon': -47.9292, 'name': 'Brasília', 'weight': 5},
    {'lat': -25.2637, 'lon': -57.5759, 'name': 'Asunción', 'weight': 4},
    {'lat': -25.2744, 'lon': -57.5359, 'name': 'Montevideo', 'weight': 4},
    
    # Africa - Comprehensive coverage
    {'lat': -26.2041, 'lon': 28.0473, 'name': 'Johannesburg', 'weight': 10, 'continent': 'Africa'},
    {'lat': -33.9249, 'lon': 18.4241, 'name': 'Cape Town', 'weight': 8},
    {'lat': 6.5244, 'lon': 3.3792, 'name': 'Lagos', 'weight': 10},
    {'lat': 30.0444, 'lon': 31.2357, 'name': 'Cairo', 'weight': 10},
    {'lat': -1.2921, 'lon': 36.8219, 'name': 'Nairobi', 'weight': 8},
    {'lat': 33.8869, 'lon': 35.5131, 'name': 'Beirut', 'weight': 5},
    {'lat': 36.8065, 'lon': 10.1815, 'name': 'Tunis', 'weight': 5},
    {'lat': 33.9716, 'lon': 6.8498, 'name': 'Algiers', 'weight': 6},
    {'lat': 14.6934, 'lon': -17.4479, 'name': 'Dakar', 'weight': 5},
    {'lat': 12.3711, 'lon': -1.5197, 'name': 'Ouagadougou', 'weight': 4},
    {'lat': 9.6412, 'lon': -13.5784, 'name': 'Conakry', 'weight': 4},
    {'lat': 8.4790, 'lon': -13.2680, 'name': 'Freetown', 'weight': 4},
    {'lat': 6.1304, 'lon': 1.2228, 'name': 'Lomé', 'weight': 4},
    {'lat': 5.3600, 'lon': -4.0083, 'name': 'Abidjan', 'weight': 5},
    {'lat': 4.3601, 'lon': 18.5542, 'name': 'Bangui', 'weight': 4},
    {'lat': 3.8480, 'lon': 11.5021, 'name': 'Yaoundé', 'weight': 5},
    {'lat': 0.3476, 'lon': 32.5825, 'name': 'Kampala', 'weight': 5},
    {'lat': -1.9403, 'lon': 30.0619, 'name': 'Kigali', 'weight': 4},
    {'lat': -4.0383, 'lon': 21.7587, 'name': 'Kinshasa', 'weight': 8},
    {'lat': -15.3875, 'lon': 28.3228, 'name': 'Lusaka', 'weight': 4},
    {'lat': -19.0154, 'lon': 29.1549, 'name': 'Harare', 'weight': 4},
    {'lat': -25.7479, 'lon': 28.2293, 'name': 'Pretoria', 'weight': 5},
    {'lat': -26.2041, 'lon': 28.0473, 'name': 'Johannesburg', 'weight': 8},
    {'lat': -29.8587, 'lon': 31.0218, 'name': 'Durban', 'weight': 5},
]

def create_weighted_cities():
    """Create weighted city list for realistic distribution"""
    weighted_cities = []
    for city in MAJOR_CITIES:
        weighted_cities.extend([city] * city['weight'])
    return weighted_cities

def generate_user_locations(total_users, centrality_data, feature_analyzer=None):
    """Generate realistic locations for ALL users with global distribution"""
    print(f"[GEOGRAPHIC] Generating fresh locations for ALL {total_users} users...")
    
    weighted_cities = create_weighted_cities()
    locations = []
    
    # Generate locations for ALL users with global distribution
    for user_id in range(total_users):
        # Choose a random city from the weighted list for global distribution
        city = random.choice(weighted_cities)
        
        # Add realistic variation around each city (±0.3 degrees for natural clustering)
        lat = city['lat'] + random.uniform(-0.3, 0.3)
        lon = city['lon'] + random.uniform(-0.3, 0.3)
        
        # Get centrality data for this user
        degree = 0
        if centrality_data and 'degree_centrality' in centrality_data:
            if isinstance(centrality_data['degree_centrality'], dict):
                degree = centrality_data['degree_centrality'].get(user_id, 0)
            elif isinstance(centrality_data['degree_centrality'], list) and user_id < len(centrality_data['degree_centrality']):
                degree = centrality_data['degree_centrality'][user_id]
        
        # Check if user has real location data
        has_real_location = False
        location_features = []
        if feature_analyzer:
            try:
                profile = feature_analyzer.get_user_profile(user_id)
                if profile and profile.get('location') and profile['location'].get('has_location'):
                    has_real_location = True
                    location_features = profile['location'].get('features', [])
            except:
                pass
        
        locations.append({
            'user_id': user_id,
            'lat': lat,
            'lon': lon,
            'degree': degree,
            'location_name': city['name'],
            'city': city['name'],
            'has_real_location': has_real_location,
            'location_features': location_features,
            'continent': city.get('continent', 'Unknown')
        })
    
    print(f"[GEOGRAPHIC] Generated {len(locations)} fresh locations successfully!")
    return locations

@geographic_bp.route('/map')
def geographic_map():
    """Serve the geographic map page - FRESH VERSION v3.0"""
    print("[GEOGRAPHIC v3.0] Serving FRESH geographic map page - CACHE BUSTED")
    return render_template('geographic_map_fresh.html')

@geographic_bp.route('/api/data')
def get_geographic_data():
    """API endpoint for geographic data with fresh generation - FRESH VERSION"""
    print("[GEOGRAPHIC API] Fresh geographic data requested")
    try:
        # Import here to avoid circular imports
        from flask import current_app
        
        # Get the analysis state from the main app
        with current_app.app_context():
            from final_app_with_checkpoints import analysis_state, feature_analyzer
            
            if not analysis_state['results']:
                return jsonify({'error': 'Analysis not complete'}), 400
            
            # Get fresh data
            total_users = analysis_state['results']['network']['nodes']
            centrality_data = analysis_state['results']['centrality']
            
            # Generate fresh locations
            locations = generate_user_locations(total_users, centrality_data, feature_analyzer)
            
            response = jsonify({
                'locations': locations,
                'total_users': len(locations),
                'cache_bust': int(time.time()),
                'fresh_generation': True
            })
            
            # Add cache-busting headers
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            
            return response
        
    except Exception as e:
        print(f"[GEOGRAPHIC ERROR] {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
