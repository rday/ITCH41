#include <stdio.h>
#include <malloc.h>

/**
This is the test for a C implementation of reading ITCH.
I'm just starting with a retrieval tree that is based on
speed. I don't have lists of child nodes, I have a static
array that works by converting the next letter of the
ticker to the offset in the array. So if the next letter
of the ticker is 'C' then we would continue to the third
element of the node list.

This is really alpha... 

Ryan Day
ryanday2@gmail.com

*/

struct node {
    char ch;                // Ticker letter
    void* value_ptr;        // Pointer to stock
    struct node* nodes[26]; // Array of possible next letters
};

struct stock {
    int price;
};

// This is tightly coupled and is meant for speed, not memory efficiency
int trie_set(struct node* root, char* key, void* value)
{
    int i = key[0] - 65;

    // If this is the last letter in our key
    if( key[1] == 0 )
    {
        root->value_ptr = value;
        return 1;
    }

    // If we have no node 
    if( root->nodes[i] == NULL )
    {
        struct node* new_node = malloc(sizeof(struct node));
        root->nodes[i] = new_node;
        return trie_set(new_node, &key[1], value);
    }

    return trie_set(root->nodes[i], &key[1], value);
}

void *trie_get(struct node* root, char* key)
{
    int i = key[0] - 65;

    // If this is our target
    if( key[1] == 0 )
        return root->value_ptr;
    if( key[i] != NULL )
        return trie_get(root->nodes[i], &key[1]);
    return NULL;
}

int main()
{
    struct node* root = malloc(sizeof(struct node));
    struct stock* cfp = malloc(sizeof(struct stock));
    struct stock* aapl = malloc(sizeof(struct stock));
    struct stock* alca = malloc(sizeof(struct stock));
    struct stock* cstr = malloc(sizeof(struct stock));

    aapl->price = 10;
    cfp->price = 20;
    alca->price = 30;
    cstr->price = 40;

    add(root, "AAPL", aapl);
    add(root, "CFP", cfp);
    add(root, "ALCA", alca);
    add(root, "CSTR", cstr);

    struct stock* s;

    s = get(root, "AAPL");
    printf("AAPL %d\n", s->price);
    cfp->price = 5;
    add(root, "AAPL", cfp);
    s = get(root, "AAPL");
    printf("AAPL %d\n", s->price);
}

