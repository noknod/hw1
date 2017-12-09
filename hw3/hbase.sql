create 'bigdatashad_yuklyushkin_profiles', 'hits', 'users', 'last_three_liked_users'

put 'bigdatashad_yuklyushkin_profiles', 'test_1', 'hits:hits', '0,1,2,3,4,5,6,7,8,9,10'
put 'bigdatashad_yuklyushkin_profiles', 'test_1', 'users:users', 'asdf'

get 'bigdatashad_yuklyushkin_profiles', 'test_1'

delete 'bigdatashad_yuklyushkin_profiles', 'test_1', 'hits:hits'
delete 'bigdatashad_yuklyushkin_profiles', 'test_1', 'users:users'

