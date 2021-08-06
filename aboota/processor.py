from home.models import News

def universally_used_data(request):
	try:
		n = News.objects.get(type='top')
		v = News.objects.get(type='down')
	except Exception as e:
		n = e
		v = e
	binary = 'BinaryTree'
	
	shop = 'Shopping.objects.get(user=rds1234)'
	dictionary_to_return = dict()
	dictionary_to_return['news'] = n
	dictionary_to_return['notification'] = v
	dictionary_to_return['bst'] = binary
	dictionary_to_return['sht'] = shop
	return dictionary_to_return