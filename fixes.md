####### views.py #######

1. fix return on RetrieveUpdateLDUDogView
    a. get_object - next to return a serializesd error for the ined error
    b. put - serialized retrun not working on Postman?

2. fix get/put on RetrieveUpdateLDUDogView
    a. URl optioanla next - will allow a PUT on get_object and bomb code 
        is there a way to check request to ensure that it is a GET

3. fix the images on lilked / dislkied / undecided 
    a. inital load of picture works but not when you return the object? is this
        the same problem as above on the return of the serialised data

4. prefernces - remove sapces

5. On first create of a registered user load all dogs against preferences with 
    undecided        


##### user.serializer #####

1. inital registration - need to log all dogs as undecided for the newly 
    registered user then he can make the decsiosns himself


               

        