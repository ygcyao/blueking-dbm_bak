package model

import (
	"database/sql"
	"fmt"
	"log/slog"
	"strings"

	"github.com/spf13/viper"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

// Database TODO
type Database struct {
	Self *gorm.DB
}

// DB TODO
var DB *Database

func OpenDB(user, password, addr, name string) *gorm.DB {
	tz := "loc=UTC&time_zone=%27%2B00%3A00%27"
	// tz := "loc=Local&time_zone=%27%2B08%3A00%27"
	dsn := fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=utf8&parseTime=%t&%s",
		user, password, addr, name, true, tz)
	sqlDB, err := sql.Open("mysql", dsn)
	if err != nil {
		slog.Error("connect to mysql failed", err)
		return nil
	}
	db, err := gorm.Open(mysql.New(mysql.Config{Conn: sqlDB}), &gorm.Config{})
	if err != nil {
		slog.Error(strings.Replace(dsn, password, "", -1))
		slog.Error(fmt.Sprintf("Database %s connection failed", name), err)
	}
	return db
}

// Init TODO
func (db *Database) Init() {
	user := viper.GetString("db.user")
	password := viper.GetString("db.password")
	host := viper.GetString("db.host")
	port := viper.GetInt("db.port")
	name := viper.GetString("db.name")
	addr := fmt.Sprintf("%s:%d", host, port)
	DB = &Database{
		Self: OpenDB(user, password, addr, name),
	}
}

func (db *Database) Close() {
	sqlDB, _ := DB.Self.DB()
	sqlDB.Close()
}
