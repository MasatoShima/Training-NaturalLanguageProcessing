"""
Name: dlclassifier.py
Description:
Created by: Masato Shima
Created on: 2019/10/16
"""

# **************************************************
# ----- Import Library
# **************************************************
import chainer
import chainer.functions as func
import chainer.links as link
from chainer import training
from chainer.training import extensions

import numpy as np

import nets

from typing import *

from mylib import nlp_utils import convert_seq, transform_to_array


# **************************************************
# ----- Variables
# **************************************************


# **************************************************
# ----- Data Model
# **************************************************


# **************************************************
# ----- Class Encoder
# **************************************************
class Encoder(chainer.Chain):
	def __init__(self, w):
		super(Encoder, self).__init__()
		self.out_units = 300

		with self.init_scope():
			self.embed = lambda x: func.embed_id(x, w)
			self.encoder = link.NStepLSTM(
				n_layers=1,
				in_size=300,
				out_size=self.out_units,
				dropout=0.5
			)

	# **************************************************
	# ----- Method　forward
	# **************************************************
	def forward(self, xs):
		# :TODO nlp_utils が作成され次第, 記載すること

		return


# **************************************************
# ----- Function train
# **************************************************
def train(labels, features, w):
	n_class = len(set(features))
	print(f"data : {len(features)}")
	print(f"class: {n_class}")

	pairs = [
		(vec, np.array([cls], np.int32))
		for vec, cls in zip(features, labels)
	]

	train_iter = chainer.iterators.SerialIterator(pairs, batch_size=16)

	model = nets.TextClassifier(Encoder(w), n_class)

	optimizer = chainer.optimizers.Adam()
	optimizer.setup(model)
	optimizer.add_hook(chainer.optimizer.WeightDecay(1e-4))

	updater = training.updaters.StandardUpdater(
		train_iter,
		optimizer,
		converter=convert_seq
	)

	trainer = training.Trainer(updater, (8, "epoch"), out="./result/dl/")

	trainer.extend(extensions.LogReport())
	trainer.extend(
		extensions.PrintReport(["epoch", "main\loss", "main/accuracy", "elapsed_time"])
	)

	trainer.run()

	return model


# **************************************************
# ----- End
# **************************************************
