# Metaphor definition

## *[Metaphor Detection in a Poetry Corpus]*

Metaphor differs from idioms, because one can understand a metaphor even with no prior knowledge 

Type I metaphor has a POS tag sequence of Noun-Verb-Noun where the verb is a copula (Neuman et al., 2013). We have extended this to include the tag sequence Noun-Verb-Det-Noun, since we have found that many instances were skipped due to the presence of a determiner. Type II has a tag sequence of Noun-Verb-Noun with a regular, not copula, verb (Neuman et al., 2013). Type III has a tag sequence of Adjective-Noun (Neuman et al., 2013). We also propose two more metaphor types that we noticed in our poetry data: Type IV with a tag sequence of Noun-Verb, and Type V with a tag sequence of Verb-Verb. Here are examples:  
- As if the world were a taxi, you enter it [Type 1] (Koch, 1962)  
- I counted the echoes assembling, thumbing the midnight on the piers. [Type 2] (Crane, 2006)  
- The moving waters at their priestlike task [Type 3] (Keats, 2009)  
- The yellow smoke slipped by the terrace, made a sudden leap [Type 4] (Eliot, 1915)  
- To die – to sleep [Type 5] (Shakespeare, 1904)


## *[Applying MIPVU Metaphor Identification Procedure on Czech]*

- Defines MIPVU for Czech
- Metaphor-related words (MRW)

Originally:

If basic meaning of a word is: 
- more concrete; what it evokes is easier to imagine, see, hear, feel, smell and taste; 
- related to bodily action; 
- more precise (as opposed to vague); 

the word is marked as MRW.

```
Take for example these expressions containing  preposition “za”. While it is clear that in sentences 3) and  4) “za” is a MRW, in the case of 1) and 2) both meanings  are clearly distinct but equally concrete and bodily related.  

1) Petr stojí za mnou; Petr stands behind me  
2) Chytil jsem ho za nohu; I caught him by the leg  
3) Za 2 roky to bude hotové; It will be done in  2 years  
4) Vyměnil jsem kolo za auto; I traded the bike for the car  

If we distinguish between “za” in instrumental (expression 1)) and in accusative 2), we can have basic meaning for  each one, moreover “accusative za” standing for basic meaning of this preposition in sentences 3) and 4) which both are MRWs.
```

I find it a bit too strict.


## MIPVU

- each word is either 0 (not a metaphor) or 1 (MRW)
    - *Each word, including function words, is annotated as metaphoric or literal*
    - *including the non-spatial meaning of in* [*An analysis of language models for metaphor recognition*]

