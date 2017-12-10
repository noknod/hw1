create 'bigdatashad_yuklyushkin_profiles', 'hits', 'users', 'last_three_liked_users'

put 'bigdatashad_yuklyushkin_profiles', 'test_2017-12-09', 'hits:hits', '0,1,2,3,4,5,6,7,8,9,10'
put 'bigdatashad_yuklyushkin_profiles', 'test_2017-12-09', 'users:users', 'asdf'

get 'bigdatashad_yuklyushkin_profiles', 'test_2017-12-09'

scan 'bigdatashad_yuklyushkin_profiles'

delete 'bigdatashad_yuklyushkin_profiles', 'test_2017-12-09', 'hits:hits'
delete 'bigdatashad_yuklyushkin_profiles', 'test_2017-12-09', 'users:users'

disable 'bigdatashad_yuklyushkin_profiles'
drop 'bigdatashad_yuklyushkin_profiles'


get 'bigdatashad_yuklyushkin_profiles', 'id10012-2017-12-06', {COLUMN => 'hits:hits', VERSIONS => 5}