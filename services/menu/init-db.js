db.auth('comp3122', '12345')
db = db.getSiblingDB('testdb')

db.createCollection('student')

db.student.insertOne({
  student_id: '33333',
  name: 'Alice',
  dept_name: 'Comp. Sci.',
  gpa: 3.1,
})
db.student.insertOne({
  student_id: '22222',
  name: 'Bob',
  dept_name: 'History.',
  gpa: 2.0,
})
db.student.insertOne({
  student_id: '11111',
  name: 'Carol',
  dept_name: 'History',
  gpa: 2.1,
})

db.createCollection('takes')
db.takes.insertOne({ student_id: '33333', course_id: 'COMP1234', credits: 1 })
db.takes.insertOne({ student_id: '22222', course_id: 'COMP1234', credits: 1 })
db.takes.insertOne({ student_id: '22222', course_id: 'COMP2345', credits: 3 })
