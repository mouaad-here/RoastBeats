import os
import json
import spotipy
import google.generativeai as genai
from django.shortcuts import render, redirect
from spotipy.oauth2 import SpotifyOAuth
from django.http import JsonResponse 

def get_spotify_oauth():
    """Helper to configure Spotify Auth"""
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        scope="user-top-read user-read-private user-read-recently-played",
    )

def get_ai_roast(username, music_profile):
    """
    Generate a roast using Google Gemini in json format.
    music_profile: String containing list of artists/tracks or user manual input.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is messing in .env")
        return None
    genai.configure(api_key=api_key)
    config = {
        "temperature": 1.0,
        "response_mime_type":"application/json",
    }
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        generation_config=config
    )
    prompt = f"""
    You are a roast comedian who specializes in stereotyping people based on their music taste. Your goal is to be unhinged, observant, and brutally funny.

    Target User: {username}
    Music profile data: "{music_profile}"
    Instructions:
    1. Identify the specific "vibes" (e.g., Sad boi, Gym bro, Indie pretender, Divorced dad energy).
    2. Make a wild, hyper-specific assumption about their personal life based on these artists.
    3. Be mean, but in a way that makes the user laugh.
    4. Do not include any Markdown formatting, no asterisks (*), no underscores (_), no backticks (`).

    Return valid JSON with these keys:
    - "headline": A short, funny archetype describing them max 4 word (e.g., "Gaslight Gatekeep Girlboss" or "Peaked in High School").
    - "score": An integer (0-100) based on you judgement.
    - "roast_body": The roast text. Use <b> to emphasize the punchline. Use <i> for sarcastic side-comments.
    - "dating_life": A "Red Flag" warning. MAX 6 WORDS. (e.g., "Will text ex at 3am", "Afraid of commitment").
    """
    try: 
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except json.JSONDecodeError:
        print("Error: AI returned Invalid JSON.")
        return fallback_roast()
    except Exception as e:
        print(f"API Error: {e}")
        return fallback_roast()

def fallback_roast():
    """Return a safe data if AI failed"""
    return {
        "headline": "Basic Taste",
        "score": 0,
        "roast_body": "The AI is speechless at your taste.",
        "dating_life": "Unknown"
    }

def index(request):
    return render(request, 'index.html')

def login(request):
    sp_auth = get_spotify_oauth()
    return redirect(sp_auth.get_authorize_url())

def callback(request):
    sp_auth = get_spotify_oauth()
    code = request.GET.get("code")

    if not code:
        return redirect('index')
    try:
        token_info = sp_auth.get_access_token(code)
        request.session['token_info'] = token_info
        # I added this to handle the roast source ( manual or spofity user)
        request.session['roast_source'] = 'spotify' 
        return redirect('roast_me')
    except Exception as e:
        print(f"Login failde: {e}")
        return redirect('index')

# ---- roast views ----

def roast_me(request):
    source =request.session.get('roast_source', 'spotify')
    context = {'trigger_ajax': True}

    try:
        if source == 'manual':
            data = request.session.get('manual_data', {})
            context['username'] = data.get('username', 'Anonymous')
            context['image'] = f"https://ui-avatars.com/api/?name={context['username']}"
        else:
            token_info = request.session.get('token_info')
            if not token_info:
                return redirect('index')
            sp = spotipy.Spotify(auth=token_info['access_token'])
            user = sp.current_user()
            context['username'] = user['display_name']
            context['image'] = user['images'][0]['url'] if user['images'] else f"https://ui-avatars.com/api/?name={user['display_name']}"
        
        return render(request, 'roast.html', context)
    except:
        return redirect('index')
    
def roast_manual(request):
    """ View for manual input Users"""
    if request.method == "POST":
        request.session['roast_source'] = 'manual'
        request.session['manual_data'] = {
            'username': request.POST.get('username', 'Anonymous'),
            'music_input': request.POST.get('music_taste', '')
        }
        return redirect('roast_me')
    return render(request, 'manual_input.html')
   
def roast_api_data(request):
    """Called by Js.It perform the slow work (spotify data + Gemini)"""
    source = request.session.get('roast_source', 'spotify')
    username = ""
    music_prompt = ""
    try:
        if source == 'manual':
            data = request.session.get('manual_data', {})
            username = data.get('username')
            music_prompt = f"{username} input: {data.get('music_input')}"
        else:
            token_info = request.session.get('token_info')
            sp = spotipy.Spotify(auth=token_info['access_token'])
            top_artists = sp.current_user_top_artists(limit=10, time_range='medium_term')
            top_tracks = sp.current_user_top_tracks(limit=10, time_range='short_term')
            artist_names = [a['name'] for a in top_artists['items']]
            track_names = [t['name'] for t in top_tracks['items']]
            username = sp.current_user()['display_name']
            music_prompt = f"Top artists: {(', '.join(artist_names))}, Top tracks: {(', ').join(track_names)}"
        
        ai_response = get_ai_roast(username, music_prompt)
        
        return JsonResponse(ai_response)
    except Exception as e:
        print(f"API Error: {e}")
        return JsonResponse(fallback_roast())
