workspace {
    name "Почтовая система"
    description "Платформа для управления электронной почтой"

    !identifiers hierarchical

    model {
        user = person "Пользователь" "Пользователь почтовой системы"
        admin = person "Администратор системы" "Управляет пользователями и следит за работой системы"
        support = person "Техподдержка" "Помогает пользователям и анализирует логи"

        user_management_system = softwareSystem "Система управления пользователями" {
            description "Управление пользователями почтовой системы"

            auth_service = container "Сервис авторизации" {
                description "Авторизация пользователей"
                technology "Python/FastAPI"
            }

            user_db = container "База данных пользователей" {
                description "Хранит данные пользователей"
                technology "PostgreSQL"
                tags "Database"
            }

            user_service = container "Сервис обработки пользователей" {
                description "Обрабатывает запросы, связанные с пользователями"
                technology "Python/FastAPI"
            }
        }

        email_management_system = softwareSystem "Система управления почтой" {
            description "Управление почтовыми папками и письмами"

            email_db = container "База данных почтовых данных" {
                description "Хранит письма и почтовые папки"
                technology "PostgreSQL"
                tags "Database"
            }

            email_service = container "Сервис почтовых сообщений" {
                description "Обрабатывает отправку, получение и управление письмами"
                technology "Python/FastAPI"
            }
        }

        monitoring_system = softwareSystem "Система мониторинга" {
            description "Отслеживание состояния системы"
            
            metrics_collector = container "Сборщик метрик" {
                description "Собирает метрики о работе сервисов и баз данных"
                technology "Prometheus"
            }
            
            visualization_dashboard = container "Дашборд мониторинга" {
                description "Отображает данные мониторинга в виде графиков и отчетов"
                technology "Grafana"
            }
            
            alerting_service = container "Сервис оповещений" {
                description "Отправляет уведомления при сбоях в системе"
                technology "Alertmanager"
            }
        }

        user -> user_management_system "Авторизация и управление учетной записью"
        user -> user_management_system.auth_service "Авторизация"
        user -> user_management_system.user_service "Настройка учетной записи"
        user -> email_management_system "Управление почтовыми папками и письмами"
        user -> email_management_system.email_service "Создает почтовые папки и получает письма"

        admin -> user_management_system "Авторизация и управление пользователями"
        admin -> user_management_system.auth_service "Авторизация"
        admin -> user_management_system.user_service "Создание и поиск пользователей"

        support -> monitoring_system "Анализирует состояние системы"
        support -> user_management_system "Помощь в управлении пользователями"
        support -> email_management_system "Помощь в работе c почтой"
        support -> monitoring_system.visualization_dashboard "Анализирует метрики системы"

        monitoring_system.metrics_collector -> email_management_system "Собирает метрики системы управления почтой"
        monitoring_system.metrics_collector -> user_management_system "Собирает метрики системы пользователей"
        monitoring_system.metrics_collector -> monitoring_system.visualization_dashboard "Передает метрики для визуализации"
        monitoring_system.metrics_collector -> monitoring_system.alerting_service "Передает метрики и события"
        monitoring_system.alerting_service -> support "Отправляет уведомления о проблемах в системе"

        user_management_system.auth_service -> user_management_system.user_service "Предоставляет доступ к сервису обработки пользователей"
        user_management_system.auth_service -> email_management_system.email_service "Предоставляет доступ к системе управления почтой"
        user_management_system.user_service -> user_management_system.user_db "Сохранение пользователей в базу данных"

        email_management_system.email_service -> email_management_system.email_db "Сохранение писем в базу данных"

        prod = deploymentEnvironment "PROD" {
            deploymentNode "User Management Server" {
                containerInstance user_management_system.auth_service
                containerInstance user_management_system.user_service
                instances 2
            }

            deploymentNode "Email Management Server" {
                containerInstance email_management_system.email_service
                instances 2
            }

            deploymentNode "Monitoring Server" {
                containerInstance monitoring_system.metrics_collector
                containerInstance monitoring_system.visualization_dashboard
                containerInstance monitoring_system.alerting_service
                instances 1
            }

            deploymentNode "Databases" {
                deploymentNode "User Database Server" {
                    containerInstance user_management_system.user_db
                    instances 2
                }

                deploymentNode "Email Database Server" {
                    containerInstance email_management_system.email_db
                    instances 2
                }
            }
        }
    }

    views {
        themes default

        properties {
            structurizr.tooltips true
        }

        systemContext user_management_system "SystemContext" "Диаграмма контекста почтовой системы" {
            autoLayout lr
            include user admin support user_management_system email_management_system monitoring_system
        }

        container user_management_system "UserManagementSystem " {
            include user admin user_management_system.auth_service user_management_system.user_service user_management_system.user_db
            autoLayout
        }

        container email_management_system "EmailManagementSystem" {
            include user email_management_system.email_service email_management_system.email_db
            autoLayout
        }

        container monitoring_system "MonitoringSystem" {
            include support monitoring_system.metrics_collector monitoring_system.visualization_dashboard monitoring_system.alerting_service
            autoLayout
        }

        deployment user_management_system "PROD" "user_management_system_prod_deployment" {
            autoLayout
            include *
        }

        deployment email_management_system "PROD" "email_management_system_prod_deployment" {
            autoLayout
            include *
        }

        deployment monitoring_system "PROD" "monitoring_system_system_prod_deployment" {
            autoLayout
            include *
        }

        dynamic user_management_system "Case1" {
            description "Создание нового пользователя"
            autoLayout
            admin -> user_management_system.auth_service "Отправляет запрос на авторизацию"
            user_management_system.auth_service -> admin "Возвращается токен"
            admin -> user_management_system.user_service "Создает нового пользователя"
            user_management_system.user_service -> user_management_system.user_db "Сохраняет данные пользователя"
        }

        dynamic user_management_system "Case2" {
            description "Поиск пользователя по логину"
            autoLayout
            admin -> user_management_system.auth_service "Отправляет запрос на авторизацию"
            user_management_system.auth_service -> admin "Возвращается токен"
            admin -> user_management_system.user_service "Ищет пользователя по логину"
            user_management_system.user_service -> user_management_system.user_db "Запрос информации о пользователе"
            user_management_system.user_db -> user_management_system.user_service "Возвращает информацию о пользователе"
            user_management_system.user_service -> admin "Передает данные о пользователе"
        }

        dynamic user_management_system "Case3" {
            description "Поиск пользователя по маске имя и фамилии"
            autoLayout
            admin -> user_management_system.auth_service "Отправляет запрос на авторизацию"
            user_management_system.auth_service -> admin "Возвращается токен"
            admin -> user_management_system.user_service "Запрос поиска пользователя по маске"
            user_management_system.user_service -> user_management_system.user_db "Поиск совпадений в базе"
            user_management_system.user_db -> user_management_system.user_service "Возвращает список пользователей"
            user_management_system.user_service -> admin "Передает результаты поиска"
        }

        dynamic email_management_system "Case4" {
            description "Создание новой почтовой папки"
            autoLayout
            user -> user_management_system.auth_service "Отправляет запрос на авторизацию"
            user_management_system.auth_service -> user "Возвращается токен"
            user -> email_management_system.email_service "Отправляет запрос на создание папки"
            email_management_system.email_service -> email_management_system.email_db "Сохраняет новую папку"
            email_management_system.email_db -> email_management_system.email_service "Подтверждение создания папки"
            email_management_system.email_service -> user "Возвращает подтверждение создания"
        }

        dynamic email_management_system "Case5" {
            description "Получение перечня всех папок"
            autoLayout
            user -> user_management_system.auth_service "Отправляет запрос на авторизацию"
            user_management_system.auth_service -> user "Возвращается токен"
            user -> email_management_system.email_service "Запрашивает список папок"
            email_management_system.email_service -> email_management_system.email_db "Получает все папки пользователя"
            email_management_system.email_db -> email_management_system.email_service "Возвращает список папок"
            email_management_system.email_service -> user "Отправляет список папок"
        }

        dynamic email_management_system "Case6" {
            description "Создание нового письма в папке"
            autoLayout
            user -> user_management_system.auth_service "Отправляет запрос на авторизацию"
            user_management_system.auth_service -> user "Возвращается токен"
            user -> email_management_system.email_service "Отправляет письмо в папку"
            email_management_system.email_service -> email_management_system.email_db "Сохраняет письмо"
            email_management_system.email_db -> email_management_system.email_service "Подтверждает сохранение"
            email_management_system.email_service -> user "Возвращает подтверждение создания письма"
        }

        dynamic email_management_system "Case7" {
            description "Получение всех писем в папке"
            autoLayout
            user -> user_management_system.auth_service "Отправляет запрос на авторизацию"
            user_management_system.auth_service -> user "Возвращается токен"
            user -> email_management_system.email_service "Запрашивает письма из папки"
            email_management_system.email_service -> email_management_system.email_db "Получает все письма в указанной папке"
            email_management_system.email_db -> email_management_system.email_service "Возвращает список писем"
            email_management_system.email_service -> user "Отправляет список писем"
        }

        dynamic email_management_system "Case8" {
            description "Получение письма по коду"
            autoLayout
            user -> user_management_system.auth_service "Отправляет запрос на авторизацию"
            user_management_system.auth_service -> user "Возвращается токен"
            user -> email_management_system.email_service "Запрашивает письмо по его коду"
            email_management_system.email_service -> email_management_system.email_db "Ищет письмо по идентификатору"
            email_management_system.email_db -> email_management_system.email_service "Возвращает письмо"
            email_management_system.email_service -> user "Отправляет письмо"
        }

        styles {
            element "SoftwareSystem" {
                background #556B2F
                color #ffffff
            }

            element "Container" {
                background #4682B4
                color #ffffff
            }

            element "Person" {
                shape Person
                background #8B0000
                color #ffffff
            }

            element "Dynamic" {
                background #FF8C00
                color #000000
            }
        }
    }
}