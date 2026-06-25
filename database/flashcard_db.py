from database.connection import connection, cursor


def insert_card(card_id: str, category: str, question: str, answer: str, hint: str):
    '''Inserts a flashcard into the database.'''
    cursor.execute(
        '''
    INSERT INTO 
        flashcards(id, category, question, answer, hint)
    VALUES 
        (?, ?, ?, ?, ?)
    ''',
        (card_id, category, question, answer, hint),
    )
    connection.commit()


def select_all_cards():
    '''Returns all flashcards.'''
    cursor.execute('''
    SELECT * 
    FROM flashcards
    ''')
    return cursor.fetchall()


def select_card_by_id(card_id: str):
    '''Returns a flashcard by id.'''
    cursor.execute(
        '''
    SELECT * 
    FROM flashcards 
    WHERE id = ?
    ''',
        (card_id,),
    )
    return cursor.fetchone()


def select_card_by_category(category: str):
    '''Returns all flashcards of a given category.'''
    cursor.execute(
        '''
    SELECT * 
    FROM flashcards 
    WHERE category = ?
    ''',
        (category,),
    )
    return cursor.fetchall()


def delete_card(card_id: str):
    '''Deletes a flashcard.'''
    cursor.execute(
        '''
    DELETE 
    FROM flashcards 
    WHERE id = ?
    ''',
        (card_id,),
    )
    connection.commit()


def update_card(category: str, question: str, answer: str, hint: str, card_id: str):
    '''Updates a flashcard by id.'''
    cursor.execute(
        '''
    UPDATE flashcards 
    SET category = COALESCE (?, category), 
        question = COALESCE (?, question),
        answer = COALESCE (?, answer),
        hint = COALESCE (?, hint)
    WHERE id = ?
    ''',
        (
            category,
            question,
            answer,
            hint,
            card_id,
        ),
    )
    connection.commit()


def select_all_categories():
    '''Returns all categories.'''
    cursor.execute('''
    SELECT DISTINCT category 
    FROM flashcards
    ''')
    return cursor.fetchall()


def delete_category(category: str):
    '''Deletes a specific category.'''
    cursor.execute(
        '''
    DELETE 
    FROM flashcards 
    WHERE category = ?
    ''',
        (category,),
    )
    connection.commit()
