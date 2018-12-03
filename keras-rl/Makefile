setup:
	pip install -r requirements.txt

play:
	export RENDER="True"; \
	python play.py

play_human:
	export HUMAN_PLAYER_MODE="True"; \
	export RENDER="True"; \
	python play.py

train:
	mkdir -p tmp
	python train.py

clean:
	rm -rf tmp

to_tf_js:
	python to_tf_js.py