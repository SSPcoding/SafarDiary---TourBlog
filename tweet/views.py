from django.shortcuts import render
from .models import Tweet, BucketList, Profile
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import ProfileUpdateForm 

# Create your views here.

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets':tweets})

@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form':form})

@login_required
def tweet_edit(request, tweet_id):
    tweet=get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form':form})

def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirmdel.html', {'tweet':tweet})

def register(request):
    if request.method == "POST":
        form  = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form':form})

def about(request):
    return render(request, 'about.html')

def feature(request):
    return render(request, 'feature.html')
    

def search_tweets(request):
    query = request.GET.get('q', '')  # Get search term
    results = Tweet.objects.filter(text__icontains=query) if query else []  # Fetch matching tweets
    
    return render(request, 'tweet_search.html', {'results': results, 'query': query})


@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    
    profile, created = Profile.objects.get_or_create(user=user)

    tweets = Tweet.objects.filter(user=user).order_by('-created_at')  # Get user's tweets

    return render(request, "profile.html", {"profile": profile, "tweets": tweets})


@login_required
def update_bio(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Ensure profile exists

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user_profile", username=request.user.username)  # Redirect to profile page
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, "update_bio.html", {"form": form})

@login_required
def add_to_bucket_list(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    bucket_list, created = BucketList.objects.get_or_create(user=request.user)

    if tweet in bucket_list.tweets.all():
        bucket_list.tweets.remove(tweet)  # If already in bucket list, remove it
    else:
        bucket_list.tweets.add(tweet)  # Add to bucket list
    
    return redirect("user_profile", username=request.user.username)

@login_required
def add_to_bucket_list(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    bucket_list, created = BucketList.objects.get_or_create(user=request.user)
    bucket_list.tweets.add(tweet)
    return redirect(request.META.get('HTTP_REFERER', 'bucket_list'))

@login_required
def remove_from_bucket_list(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    bucket_list, created = BucketList.objects.get_or_create(user=request.user)
    bucket_list.tweets.remove(tweet)
    return redirect(request.META.get('HTTP_REFERER', 'bucket_list'))


@login_required
def view_bucket_list(request):
    bucket_list, created = BucketList.objects.get_or_create(user=request.user)
    return render(request, "bucket_list.html", {"tweets": bucket_list.tweets.all()})
