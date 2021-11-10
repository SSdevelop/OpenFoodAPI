db.auth('comp3122', '12345')
db = db.getSiblingDB('menu')

db.createCollection('item', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['id', 'title', 'price'],
      properties: {
        id: {
          bsonType: 'string',
          uniqueItems: true,
          description: 'Must be unique string and is required',
        },
        description: {
          bsonType: 'string',
          description:
            '(optional) Supplementary information describing the item (by locale).',
        },
        title: {
          bsonType: 'string',
          description: 'The name of the item (by locale).',
        },
        price: {
          bsonType: 'in',
          description: 'City; Required',
        },
      },
    },
  },
})

db.createCollection('menu', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['id', 'title', 'price'],
      properties: {
        id: {
          bsonType: 'string',
          uniqueItems: true,
          description: 'Must be unique string and is required',
        },
        title: {
          bsonType: 'string',
          description: 'The name of the men (by locale).',
        },
        subtitle: {
          bsonType: 'string',
          description: 'An optional subtitle for the menu (by locale).',
        },
        // service_availablity: {
        //   bsonType: "object",
        //   required: [],
        //   properties:{
        //     day_of_week: "",
        //   }
        // },
      },
    },
  },
})

db.createCollection('category', {
  validator: {
    $jsoSchema: {
      bsonType: 'object',
      required: [],
      properties: {
        id: {
          bsonType: 'string',
          description: 'Must be unique string and is required',
        },
        entities: {
          bsonType: ['array'],
          items: {
            bsonType: 'object',
            required: ['type', 'id'],
            properties: {
              id: {
                bsonType: 'string',
                description: 'must be a string and is required',
              },
              type: {
                bsonType: 'string',
                description: 'must be a string and is required',
              },
            },
          },
          description: 'array of items ',
        },
        title: {
          bsonType: 'string',
          description: 'The name of the men (by locale).',
        },
      },
    },
  },
})

db.menu.insertOne({
  id: 'empty_menu_id',
  title: {
    translations: {
      en_us: 'Empty Menu',
    },
  },
  service_availability: [
    {
      day_of_week: 'monday',
      time_periods: [{ start_time: '00:00', end_time: '23:59' }],
    },
    {
      day_of_week: 'tuesday',
      time_periods: [{ start_time: '00:00', end_time: '23:59' }],
    },
    {
      day_of_week: 'wednesday',
      time_periods: [{ start_time: '00:00', end_time: '23:59' }],
    },
    {
      day_of_week: 'thursday',
      time_periods: [{ start_time: '00:00', end_time: '23:59' }],
    },
    {
      day_of_week: 'friday',
      time_periods: [{ start_time: '00:00', end_time: '23:59' }],
    },
    {
      day_of_week: 'saturday',
      time_periods: [{ start_time: '00:00', end_time: '23:59' }],
    },
    {
      day_of_week: 'sunday',
      time_periods: [{ start_time: '00:00', end_time: '23:59' }],
    },
  ],
  category_ids: [],
})

db.createCollection('takes')
db.takes.insertOne({ student_id: '33333', course_id: 'COMP1234', credits: 1 })
db.takes.insertOne({ student_id: '22222', course_id: 'COMP1234', credits: 1 })
db.takes.insertOne({ student_id: '22222', course_id: 'COMP2345', credits: 3 })
