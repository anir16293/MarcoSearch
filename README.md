# MarcoSearch

Winner of the Microsoft Marco track at HopHacks 2019.

MarcoSearch is an efficient way to get multi-perspective information on a topic by extracting information through multi-lingual online resources and translating them back to English.

MarcoSearch works as follows:

1) Translate the target query into a set of languages.
2) Run a language-specific Google search on the translated set of queries.
3) Translate the pages back into English.
4) Use Microsoft's MS Marco API to obtain embeddings for the original search query and all the translated documents.
5) Rank the websites based on a similarity score between the query embeddings and the document embeddings.
6) Generate the top N results.
