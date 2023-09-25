from django.contrib import admin
from .models import Book, BookInstance, Author, Genre, Language

# Register your models here.
admin.site.register([Genre,Language])

# Stacked means show fields vertically
class BookInline(admin.StackedInline):
    model = Book
    # No extra lines to add a new Book - just listing the existing ones
    extra = 0

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # UpdateView - a tuple groups fields horizontally
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    # UpdateView - to be able to add Books while Updating the Author
    inlines = [BookInline]

admin.site.register(Author, AuthorAdmin)

# Tabular means show fields horizontally
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

# Decorator ~ admin.site.register(model, subclass of a ModelAdmin)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    # UpdateView - to be able to add BookInstances while Updating the Book
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'imprint', 'status', 'due_back', 'borrower')
    list_filter = ('status', 'due_back', 'borrower')

    # UpdateView - grouping fields into sections
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        })
    )