from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences1 = ['The cat sits outside',
              'A man is playing guitar',
              'The movies are awesome']
embedding1 = model.encode(sentences1)


print(embedding1.shape)
print(embedding1)

sentences2 = ['The dog plays in the garden',
              'A woman watches TV',
              'The new movie is so great']

embedding2 = model.encode(sentences2)

print(embedding1.shape)
print(embedding1)

cosine_scores = util.cos_sim(embedding1,embedding2)

print(cosine_scores)

for i in range(len(sentences1)):
    print("Sentence 1:", sentences1[i])
    print("Sentence 2:", sentences2[i])
    print(f"Similarity score: {cosine_scores[i][i]:.4f}")
    print("-" * 40)