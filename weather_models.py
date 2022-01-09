import mongoengine as me

me.connect('weather_db1')

class Gallary(me.Document):
    title = me.StringField(required = True, min_length = 2)
    image = me.FileField(required = True)
    @classmethod
    def get_weather_img(cls, title):
        return cls.objects.get(title = title)

if __name__ == "__main__":
    list_of_images = ['partial_clouds.jpg', 'Sunny_weather.jpg', 'Thunder_clouds.jpeg', 'Thunder_storm.jpg']
    for img in list_of_images:
        with open(img, 'rb') as image:
            photo = Gallary(title = f'{img}')
            photo.image.put(image, content_type = 'image/jpeg')
            photo.save()