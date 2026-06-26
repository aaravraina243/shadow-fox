import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# loading the dataset
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.cifar10.load_data()

# Normalization of pixerls
train_images, test_images = train_images / 255.0, test_images / 255.0

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
               'dog', 'frog', 'horse', 'ship', 'truck']
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10) 
])
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
# training part 
print("Starting training...")
history = model.fit(train_images, train_labels, epochs=10, 
                    validation_data=(test_images, test_labels))
# Result
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
print(f"\nTest Accuracy: {test_acc:.2f}")