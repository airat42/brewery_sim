from django.contrib import admin
from .models import Hop, Malt, Yeast, Recipe, Beer, GameState, Smell, BitterSmell, MaltInventory, HopInventory, YeastInventory
from .models import Mill, Brewer, Tank, Container, BrewerInventory

admin.site.register(Malt)
admin.site.register(Yeast)
admin.site.register(Recipe)
admin.site.register(Beer)
admin.site.register(GameState)
admin.site.register(Smell)

@admin.register(Mill)
class MillAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Brewer)
class BrewerAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Tank)
class TankAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(BitterSmell)
class BitterSmellAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(MaltInventory)
class MaltInventoryAdmin(admin.ModelAdmin):
    list_display = ("malt",)

@admin.register(HopInventory)
class HopInventoryAdmin(admin.ModelAdmin):
    list_display = ("hop",)

@admin.register(YeastInventory)
class YeastInventoryAdmin(admin.ModelAdmin):
    list_display = ("yeast",)

@admin.register(Hop)
class HopAdmin(admin.ModelAdmin):
    list_display = ('name', 'a_acid', 'b_acid', 'smell', 'bitter_or_smell')
    # list_filter = ('name', 'a_acid')
    # list_editable = ('name', 'a_acid')

@admin.register(BrewerInventory)
class BrewerInventoryAdmin(admin.ModelAdmin):
    list_display = ("brewer",)