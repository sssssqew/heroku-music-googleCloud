from django.contrib import admin

# admin 뒤에 / 붙여야 어드민 사이트 나옴
# Register your models here.
from .models import AudioFile

class AudioFileAdmin(admin.ModelAdmin):
    list_display = ['song', 'name'] # 커스터마이징 코드
    list_filter = ('song', 'name', )
    search_fields = ['name']


admin.site.register(AudioFile, AudioFileAdmin)