db.auth('menu', 'pass')
db = db.getSiblingDB('menus')

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
        store_id: {
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
      required: ['id', 'title'],
      properties: {
        id: {
          bsonType: 'string',
          uniqueItems: true,
          description: 'Must be unique string and is required',
        },
        store_id: {
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
        //   bsonType: ['array'],
        //   required: [],
        //   properties: {
        //     time_periods: '',
        //     day_of_week: '',
        //   },
        // },
        category_ids: {
          bsonType: ['array'],
          description:
            'All of the IDs for the menu categories that will be made available while this menu is active.',
          items: {
            bsonType: 'string',
          },
        },
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
        store_id: {
          bsonType: 'string',
          uniqueItems: true,
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
  store_id: 'ecs_ny',
  title: 'Empty Menu',
  subtitle: 'Empty Meny Subtitle',
  category_ids: ['Sandwiches', 'Snacks'],
})

db.item.insertMany([
  {
    id: 'Coffee2',
    store_id: 'ecs_ny',
    description: 'Deliciously roasted beans 2',
    title: 'Coffee',
    price: 300,
  },
  {
    id: 'Blueberry',
    store_id: 'ecs_ny',
    description: 'Delicious Blueberry',
    title: 'Blueberry',
    price: 5,
  },
  {
    id: 'Muffin',
    store_id: 'ecs_ny',
    description: 'Great for afternoon snack time!',
    title: 'Fresh-baked muffin',
    price: 5,
  },
  {
    id: 'Chicken-sandwich',
    store_id: 'ecs_ny',
    description: 'Deliciously roasted beans',
    title: 'Blueberry',
    price: 5,
  },
])

db.category.insertMany([
  {
    entities: [
      {
        type: 'ITEM',
        id: 'Muffin',
      },
    ],
    id: 'Snacks',
    title: 'Snacks',
    store_id: 'ecs_ny',
  },
  {
    entities: [
      {
        type: 'ITEM',
        id: 'Chicken-sandwich',
      },
    ],
    id: 'Sandwiches',
    title: 'Sandwiches',
    store_id: 'ecs_ny',
  },
])
