// Autogenerated from repository.template file at 18/03/2021 21:47:35
package com.example.demo.generated.repositories;

import com.example.demo.generated.models.Author;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;

@Repository
public interface AuthorRepository extends JpaRepository<Author, Long> {
    Author getAuthorById(Long id);
}