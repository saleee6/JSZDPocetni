// Autogenerated from entity.template file at 18/03/2021 19:13:47
package com.example.demo.generated.models;

import javax.persistence.*;
import java.util.*;

@Entity
class Book {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column  private String isbn;

  @OneToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL) 
  private Author author;

  @Column  private String title;

  public Book() {
 
  }

  public Long getId(){
    return this.id;
  }

  public String getIsbn(){
    return this.isbn;
  }

  public void setIsbn(String new_value){
    this.isbn = new_value;
  }
  public Author getAuthor(){
    return this.author;
  }

  public void setAuthor(Author new_value){
    this.author = new_value;
  }
  public String getTitle(){
    return this.title;
  }

  public void setTitle(String new_value){
    this.title = new_value;
  }
}