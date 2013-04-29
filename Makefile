
.PHONY: install
install:
	pip install -r requirements.txt --use-mirrors
	python setup.py develop

.PHONY: tx
tx:
	mkdir -p opps/polls/locale/en_US/LC_MESSAGES
	touch opps/polls/locale/en_US/LC_MESSAGES/django.po
	tx set --auto-remote https://www.transifex.com/projects/p/opps/resource/polls/
	tx set --auto-local -r opps.polls "opps/polls/locale/<lang>/LC_MESSAGES/django.po" --source-language=en_US --source-file "opps/polls/locale/en_US/LC_MESSAGES/django.po" --execute
	tx pull -f
