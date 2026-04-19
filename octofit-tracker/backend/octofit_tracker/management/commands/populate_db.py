from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Team.objects.all().delete()
        for user in User.objects.filter(is_superuser=False):
            user.delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users (super heroes)
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': marvel},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'team': marvel},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': dc},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': dc},
        ]
        user_objs = []
        for u in users:
            user = User.objects.create_user(username=u['username'], email=u['email'], password='password')
            u['team'].members.add(user)
            user_objs.append(user)

        # Create workouts
        workout1 = Workout.objects.create(name='Pushups', description='Do 20 pushups', difficulty='Easy')
        workout2 = Workout.objects.create(name='Running', description='Run 5km', difficulty='Medium')
        workout1.suggested_for.set(user_objs)
        workout2.suggested_for.set(user_objs)

        # Create activities
        Activity.objects.create(user=user_objs[0], activity_type='Pushups', duration=10, calories_burned=50, date=timezone.now().date(), team=marvel)
        Activity.objects.create(user=user_objs[1], activity_type='Running', duration=30, calories_burned=200, date=timezone.now().date(), team=marvel)
        Activity.objects.create(user=user_objs[2], activity_type='Pushups', duration=15, calories_burned=70, date=timezone.now().date(), team=dc)
        Activity.objects.create(user=user_objs[3], activity_type='Running', duration=25, calories_burned=180, date=timezone.now().date(), team=dc)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
